// Edge Function "nhac-viec": mỗi phút được pg_cron gọi, gửi Telegram cho sự kiện đến giờ nhắc.
// Secrets cần (Supabase > Edge Functions > Secrets): TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, CRON_KEY.
// SUPABASE_URL và SUPABASE_SERVICE_ROLE_KEY có sẵn tự động. Tắt "Verify JWT" cho function này (đã có CRON_KEY bảo vệ).
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

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

Deno.serve(async (req) => {
  if (req.headers.get('x-cron-key') !== Deno.env.get('CRON_KEY')) return new Response('forbidden', { status: 403 });
  const sb = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!);
  const token = Deno.env.get('TELEGRAM_BOT_TOKEN')!, chat = Deno.env.get('TELEGRAM_CHAT_ID')!;
  const now = Date.now();
  const { data, error } = await sb.from('su_kien').select('*').is('xoa_luc', null).not('nhac_phut', 'is', null);
  if (error) return new Response(error.message, { status: 500 });
  let daGui = 0; const loi: string[] = [];
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
      const res = await fetch(`https://api.telegram.org/bot${token}/sendMessage`, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ chat_id: chat, text }),
      });
      if (res.ok) daGui++;
      else { loi.push(`${r.id}: Telegram ${res.status}`); await sb.from('nhac_da_gui').delete().eq('su_kien_id', r.id).eq('lan', new Date(t).toISOString()); }
    }
  }
  return new Response(JSON.stringify({ daGui, loi }), { headers: { 'Content-Type': 'application/json' } });
});
