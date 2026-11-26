// Edge Function "ban-tin-gui" (giai đoạn 2.9): dựng BẢN TIN SÁNG (lấy tin -> Gemini dịch/tóm tắt -> phần đầu) -> lưu bảng ban_tin -> gửi Telegram.
// - pg_cron gọi lúc 8:00 giờ VN (header x-cron-key): dựng + lưu + gửi Telegram.
// - Nút "Tạo bản tin hôm nay" trong app (token chủ app, body {"chi_tao":true}): dựng + lưu, KHÔNG gửi Telegram. {"ep":true} = tạo lại dù đã có.
// - Chống gửi trùng: đã gửi Telegram hôm nay thì không gửi lại (trừ ep:true). Đã có bản tin mà chưa gửi được (lỗi trước đó) thì chỉ gửi lại, không tạo lại.
// Secrets cần: GEMINI_API_KEY, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CRON_KEY (đều đã có ở 2.5/2.7). SUPABASE_URL / SUPABASE_ANON_KEY / SUPABASE_SERVICE_ROLE_KEY có sẵn.
// Cần function "ban-tin-lay" đã deploy (function này gọi nó qua HTTP bằng x-cron-key, nên KHÔNG cần import chéo thư mục).
// Deploy: tắt "Verify JWT" (function tự kiểm quyền).
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { catNgan, dungNoiDung, dungPhanDau, dungVanBanTelegram, chonUngVien, goiGemini, ngayVN } from './loi.ts';
import type { KetQuaGemini, KetQuaLay, NoiDung } from './loi.ts';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-cron-key',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', ...CORS } });
const msg = (e: unknown) => (e instanceof Error ? e.message : String(e));

// Lấy tin qua function ban-tin-lay (HTTP). Lỗi -> trả {tin:{}, loi:[lý do]} để vẫn có bản tin (chỉ phần đầu).
async function layTin(): Promise<{ kq: KetQuaLay; loi: string | null }> {
  try {
    const url = `${Deno.env.get('SUPABASE_URL')}/functions/v1/ban-tin-lay`;
    const r = await fetch(url, { method: 'POST', headers: { 'x-cron-key': Deno.env.get('CRON_KEY') || '', 'Content-Type': 'application/json' }, body: '{}', signal: AbortSignal.timeout(45000) });
    if (!r.ok) return { kq: { tin: {} }, loi: `ban-tin-lay trả lỗi ${r.status}` + (r.status === 404 ? ' (chưa deploy function ban-tin-lay?)' : '') };
    const j = await r.json();
    if (!j || typeof j.tin !== 'object' || j.tin === null) return { kq: { tin: {} }, loi: 'ban-tin-lay trả dữ liệu lạ' };
    return { kq: j as KetQuaLay, loi: null };
  } catch (e) { return { kq: { tin: {} }, loi: 'Không gọi được ban-tin-lay: ' + msg(e) }; }
}

// Gửi Telegram lần lượt từng khúc. Trả về null nếu thành công hết, hoặc mô tả lỗi.
async function guiTelegram(khuc: string[]): Promise<string | null> {
  const token = Deno.env.get('TELEGRAM_BOT_TOKEN'), chat = Deno.env.get('TELEGRAM_CHAT_ID');
  if (!token || !chat) return 'Chưa cài TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID';
  for (let i = 0; i < khuc.length; i++) {
    try {
      const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ chat_id: chat, text: khuc[i], parse_mode: 'HTML', disable_web_page_preview: true }),
        signal: AbortSignal.timeout(20000),
      });
      if (!res.ok) return `Telegram ${res.status} ở khúc ${i + 1}/${khuc.length}`;
    } catch (e) { return `Telegram lỗi mạng ở khúc ${i + 1}/${khuc.length}: ${msg(e)}`; }
  }
  return null;
}

Deno.serve(async (req: Request) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  if (req.method !== 'POST') return json({ loi: 'Chỉ nhận yêu cầu POST' }, 405);
  // 1) Quyền: pg_cron (x-cron-key) hoặc chủ app đã đăng nhập
  const cron = req.headers.get('x-cron-key');
  if (cron) {
    const khoa = Deno.env.get('CRON_KEY');
    if (!khoa || cron !== khoa) return new Response('forbidden', { status: 403 });
  } else {
    const auth = req.headers.get('authorization') || '';
    if (!auth.startsWith('Bearer ')) return json({ loi: 'Bạn cần đăng nhập lại' }, 401);
    const nguoi = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
    const { data: chu, error } = await nguoi.rpc('la_chu_app');
    if (error || chu !== true) return json({ loi: 'Chỉ chủ app được tạo bản tin' }, 403);
  }
  let body: { ep?: boolean; chi_tao?: boolean } = {};
  try { body = await req.json(); } catch (_) { body = {}; }
  const ep = !!(body && body.ep), chiTao = !!(body && body.chi_tao);

  try {
    const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
    const now = Date.now(), ngay = ngayVN(now);
    const cu = await sb.from('ban_tin').select('ngay,noi_dung,telegram_luc').eq('ngay', ngay).maybeSingle();
    if (cu.error) return json({ loi: 'Đọc bảng ban_tin lỗi: ' + cu.error.message + ' (đã chạy sql/2.9-ban-tin.sql chưa?)' }, 500);
    const co = cu.data as { noi_dung: NoiDung; telegram_luc: string | null } | null;

    let nd: NoiDung | null = co ? co.noi_dung : null;
    let taoMoi = false;
    const ghiChu: string[] = [];
    // 2) Dựng bản tin nếu chưa có (hoặc ép tạo lại)
    if (!co || ep) {
      const lay = await layTin();
      const [sk, yt] = await Promise.all([
        sb.from('su_kien').select('tieu_de,bat_dau,ket_thuc,ca_ngay,lap,lap_den,lap_ngoai').is('xoa_luc', null),
        sb.from('y_tuong').select('tieu_de,trang_thai,han,sua_luc,xoa_luc').is('xoa_luc', null),
      ]);
      if (sk.error) ghiChu.push('Đọc lịch lỗi: ' + sk.error.message);
      if (yt.error) ghiChu.push('Đọc ý tưởng lỗi: ' + yt.error.message);
      const dau = dungPhanDau(sk.data || [], yt.data || [], now);
      const uv = chonUngVien(lay.kq.tin || {});
      // đúng 1 lần gọi Gemini (tối đa 2 nếu lỗi tạm thời); lỗi gì cũng không chặn bản tin
      let gem: KetQuaGemini | null = null;
      if (uv.length) {
        try { gem = await goiGemini(uv, Deno.env.get('GEMINI_API_KEY')); }
        catch (e) { gem = { ok: false, loai: 'tam_thoi', ly_do: 'Gemini lỗi bất ngờ: ' + msg(e), so_lan: 1 }; }
      }
      const loiNguon = [...(lay.kq.loi || [])];
      if (lay.loi) loiNguon.unshift(lay.loi);
      nd = dungNoiDung(ngay, now, dau, uv, gem, loiNguon);
      if (!nd.dung_ai && nd.ly_do_khong_ai) ghiChu.push('Gemini: ' + nd.ly_do_khong_ai);
      const hang = { noi_dung: nd, tao_luc: new Date(now).toISOString(), loi: ghiChu.join('; ') || null };
      const luu = co ? await sb.from('ban_tin').update(hang).eq('ngay', ngay) : await sb.from('ban_tin').insert({ ngay, ...hang });
      if (luu.error) return json({ loi: 'Lưu bản tin lỗi: ' + luu.error.message }, 500);
      taoMoi = true;
    }
    if (!nd) return json({ loi: 'Không có bản tin' }, 500);

    // 3) Telegram: chỉ khi cron/không chi_tao, và (chưa gửi hôm nay hoặc ép)
    let daGui = !!(co && co.telegram_luc), loiTg: string | null = null, guiLanNay = false;
    if (!chiTao && (ep || !co || !co.telegram_luc)) {
      loiTg = await guiTelegram(dungVanBanTelegram(nd));
      if (!loiTg) { daGui = true; guiLanNay = true; await sb.from('ban_tin').update({ telegram_luc: new Date().toISOString() }).eq('ngay', ngay); }
      else { ghiChu.push(loiTg); await sb.from('ban_tin').update({ loi: ghiChu.join('; ') }).eq('ngay', ngay); } // bản tin đã lưu vẫn còn
    }
    return json({
      ngay, tao_moi: taoMoi, so_tin: nd.tin.length, dung_ai: nd.dung_ai, ly_do_khong_ai: nd.ly_do_khong_ai,
      so_lan_gemini: nd.so_lan_gemini, loi_nguon: nd.loi_nguon, da_gui: daGui, gui_lan_nay: guiLanNay, loi_telegram: loiTg,
      ghi_chu: catNgan(ghiChu.join('; '), 300) || null,
    });
  } catch (e) {
    return json({ loi: 'Tạo bản tin gặp lỗi: ' + msg(e) }, 500);
  }
});
