// Edge Function "nhac-viec": mỗi phút được pg_cron gọi, gửi Telegram cho sự kiện đến giờ nhắc.
// Gửi cả Telegram (dự phòng) lẫn thông báo đẩy Web Push (2.5b) tới mọi thiết bị trong bảng push_dang_ky.
// Secrets cần (Supabase > Edge Functions > Secrets): TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CRON_KEY,
//   VAPID_PUBLIC_KEY, VAPID_PRIVATE_KEY, VAPID_SUBJECT (mailto:...).
// SUPABASE_URL và SUPABASE_SERVICE_ROLE_KEY có sẵn tự động. Tắt "Verify JWT" cho function này (đã có CRON_KEY bảo vệ).
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import webpush from 'npm:web-push@3.6.7';

const VN = 7 * 3600000; // Việt Nam UTC+7, không đổi giờ mùa
const CUA_SO = 10 * 60000; // bù tối đa 10 phút nếu một lần chạy bị lỡ

type Row = {
  id: string; tieu_de: string; ghi_chu: string | null; bat_dau: string; ket_thuc: string; ca_ngay: boolean;
  lap: string; lap_den: string | null; lap_ngoai: string[] | null; nhac_phut: number;
};

// Các lần bắt đầu (mili giây UTC) của sự kiện nằm trong [from, to]
function cacLan(r: Row, from: number, to: number): number[] {
  const s = new Date(r.bat_dau).getTime();
  const out: number[] = [];
  if (!r.lap || r.lap === 'none') { if (s >= from && s <= to) out.push(s); return out; }
  const ngoai = (r.lap_ngoai || []).map((x) => new Date(x).getTime());
  const den = r.lap_den; // 'YYYY-MM-DD' theo giờ VN
  const ok = (t: number) => t >= from && t <= to && t >= s && !ngoai.includes(t) &&
    !(den && new Date(t + VN).toISOString().slice(0, 10) > den);
  if (r.lap === 'month') {
    const sv = new Date(s + VN);
    for (let k = 0; k < 6000; k++) {
      const d = new Date(Date.UTC(sv.getUTCFullYear(), sv.getUTCMonth() + k, sv.getUTCDate(), sv.getUTCHours(), sv.getUTCMinutes(), sv.getUTCSeconds()));
      if (d.getUTCDate() !== sv.getUTCDate()) continue; // tháng không có ngày này (vd 31)
      const t = d.getTime() - VN;
      if (t > to) break;
      if (ok(t)) out.push(t);
    }
    return out;
  }
  const buoc = (r.lap === 'week' ? 7 : 1) * 86400000;
  for (let t = s + Math.max(0, Math.ceil((from - s) / buoc)) * buoc; t <= to; t += buoc) if (ok(t)) out.push(t);
  return out;
}

const gio = (t: number) => new Date(t + VN).toISOString().slice(11, 16);
const ngay = (t: number) => { const d = new Date(t + VN).toISOString().slice(0, 10).split('-'); return `${d[2]}/${d[1]}/${d[0]}`; };

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-cron-key',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', ...CORS } });

// Gửi Web Push tới mọi thiết bị đã đăng ký. KHÔNG BAO GIỜ ném lỗi ra ngoài (lỗi push không được chặn Telegram / chống trùng).
// Đăng ký chết (404/410) bị xoá. Trả về { gui, chet, loi }.
async function guiPush(sb: any, payload: { title: string; body: string; tag: string; url?: string }) {
  const kq = { gui: 0, chet: 0, loi: [] as string[] };
  try {
    const pub = Deno.env.get('VAPID_PUBLIC_KEY'), pri = Deno.env.get('VAPID_PRIVATE_KEY');
    const sub = Deno.env.get('VAPID_SUBJECT') || 'mailto:harry-ai@users.noreply.github.com';
    if (!pub || !pri) { kq.loi.push('Chưa đặt secrets VAPID'); return kq; }
    webpush.setVapidDetails(sub, pub, pri);
    const { data, error } = await sb.from('push_dang_ky').select('id,endpoint,p256dh,auth');
    if (error) { kq.loi.push('Đọc push_dang_ky: ' + error.message); return kq; }
    const body = JSON.stringify({ ...payload, url: payload.url || './' });
    await Promise.all((data || []).map(async (d: any) => {
      try {
        await webpush.sendNotification({ endpoint: d.endpoint, keys: { p256dh: d.p256dh, auth: d.auth } }, body, { TTL: 3600, urgency: 'high' });
        kq.gui++;
      } catch (e: any) {
        if (e && (e.statusCode === 404 || e.statusCode === 410)) {
          kq.chet++;
          try { await sb.from('push_dang_ky').delete().eq('id', d.id); } catch (_) { /* bỏ qua */ }
        } else kq.loi.push(`Push ${e && e.statusCode ? e.statusCode : ''} ${e && e.message ? e.message : e}`.trim());
      }
    }));
  } catch (e: any) { kq.loi.push('Push: ' + (e && e.message ? e.message : e)); }
  return kq;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  // Chế độ "Gửi thử" từ trang Cài đặt: người dùng đã đăng nhập + là chủ app (kiểm bằng chính token của họ), chỉ gửi push, không Telegram.
  const auth = req.headers.get('authorization') || '';
  if (!req.headers.get('x-cron-key') && auth.startsWith('Bearer ')) {
    const nguoi = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
    const { data: chu, error: e1 } = await nguoi.rpc('la_chu_app');
    if (e1 || chu !== true) return json({ loi: 'Chỉ chủ app được gửi thử' }, 403);
    const kq = await guiPush(sb, { title: '🔔 Harry AI', body: 'Thông báo thử — nếu bạn thấy dòng này là đã bật thành công.', tag: 'thu' });
    return json({ thu: true, ...kq });
  }
  if (req.headers.get('x-cron-key') !== Deno.env.get('CRON_KEY')) return new Response('forbidden', { status: 403 });
  const token = Deno.env.get('TELEGRAM_BOT_TOKEN')!, chat = Deno.env.get('TELEGRAM_CHAT_ID')!;
  const now = Date.now();
  const { data, error } = await sb.from('su_kien').select('*').is('xoa_luc', null).not('nhac_phut', 'is', null);
  if (error) return new Response(error.message, { status: 500 });
  let daGui = 0, pushGui = 0, pushChet = 0; const loi: string[] = [];
  for (const r of (data || []) as Row[]) {
    const off = r.ca_ngay ? 8 * 3600000 : 0; // sự kiện cả ngày: tính từ 8:00 sáng
    const nh = r.nhac_phut * 60000;
    // Lần nào có (giờ_bắt_đầu + off − nhắc) rơi trong (now − 10 phút, now]
    for (const t of cacLan(r, now - CUA_SO - off + nh, now - off + nh)) {
      const dauNhac = t + off - nh;
      if (dauNhac > now || dauNhac <= now - CUA_SO) continue;
      const ins = await sb.from('nhac_da_gui').insert({ su_kien_id: r.id, lan: new Date(t).toISOString() });
      if (ins.error) continue; // đã gửi rồi (trùng khoá) hoặc lỗi → bỏ qua
      const khi = r.ca_ngay ? `cả ngày ${ngay(t)}` : r.nhac_phut === 0 ? `bây giờ (${gio(t)})` : `lúc ${gio(t)} ${ngay(t)}`;
      const text = `🔔 ${r.tieu_de}\n${r.nhac_phut > 0 && !r.ca_ngay ? `Còn ${r.nhac_phut >= 60 && r.nhac_phut % 60 === 0 ? r.nhac_phut / 60 + ' giờ' : r.nhac_phut + ' phút'} — ` : ''}${khi}${r.ghi_chu ? '\n' + r.ghi_chu : ''}`;
      // Push chạy song song, mọi lỗi đã được nuốt trong guiPush → Telegram luôn được gửi
      const pushP = guiPush(sb, { title: '🔔 ' + r.tieu_de, body: text.split('\n').slice(1).join('\n'), tag: `nhac-${r.id}-${t}` });
      let res: Response | null = null;
      try {
        res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
          method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ chat_id: chat, text }),
        });
      } catch (_) { res = null; }
      const kqPush = await pushP;
      pushGui += kqPush.gui; pushChet += kqPush.chet; loi.push(...kqPush.loi.map((x) => `${r.id}: ${x}`));
      // Đã có ít nhất một kênh đến nơi thì coi là đã nhắc (không nhắc lại); cả hai hỏng mới xoá dấu để thử lại
      if (res && res.ok) daGui++;
      else if (kqPush.gui > 0) { daGui++; loi.push(`${r.id}: Telegram ${res ? res.status : 'lỗi mạng'} (push đã gửi)`); }
      else {
        loi.push(`${r.id}: Telegram ${res ? res.status : 'lỗi mạng'}`); await sb.from('nhac_da_gui').delete().eq('su_kien_id', r.id).eq('lan', new Date(t).toISOString()); }
    }
  }
  return json({ daGui, pushGui, pushChet, loi });
});
