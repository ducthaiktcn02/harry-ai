// Chạy THẬT một phần của 2.9: tải RSS thật (miễn phí) -> chọn ứng viên -> (nếu có GEMINI_API_KEY) ĐÚNG 1 lần gọi Gemini thật để kiểm schema
// -> dựng bản tin + văn bản Telegram. KHÔNG gửi Telegram, KHÔNG chạm Supabase. Không in khoá.
// Chạy (PowerShell): $env:GEMINI_API_KEY = [Environment]::GetEnvironmentVariable('GEMINI_API_KEY','User'); deno run --allow-net --allow-env --allow-write tools/chay_that_ban_tin_gui.ts
import { HAN_CHOT_MS, NGUON } from '../supabase/functions/ban-tin-lay/nguon.ts';
import { layTatCa } from '../supabase/functions/ban-tin-lay/loi.ts';
import { chonUngVien, dungNoiDung, dungPhanDau, dungVanBanTelegram, goiGemini } from '../supabase/functions/ban-tin-gui/loi.ts';

async function tai(url: string): Promise<string> {
  let loi: unknown;
  for (let i = 0; i < 2; i++) {
    try {
      const r = await fetch(url, { signal: AbortSignal.timeout(HAN_CHOT_MS), headers: { 'User-Agent': 'Mozilla/5.0 (compatible; HarryAI-BanTin/1.0)', Accept: 'application/rss+xml, application/xml, text/xml, */*' } });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.text();
    } catch (e) { loi = e; }
  }
  throw loi;
}
const now = Date.now();
const lay = await layTatCa(NGUON, tai, now);
const uv = chonUngVien(lay.tin);
const d: string[] = [`Chạy thật lúc ${new Date(now).toISOString()}: RSS ${lay.dem.tong} tin (${lay.dem.nguon_ok}/${NGUON.length} nguồn OK) -> ${uv.length} ứng viên gửi Gemini`];
d.push('Ứng viên theo chủ đề: ' + Object.entries(Object.groupBy(uv, (u) => u.chu_de)).map(([k, v]) => `${k}=${v!.length}`).join(', '));

// Đúng 1 lần gọi Gemini thật: hàm fetch bọc lại, lần gọi thứ 2 bị chặn
let soGoi = 0;
const fetchMotLan = ((u: string, i: RequestInit) => { if (++soGoi > 1) return Promise.reject(new Error('Chặn: không gọi Gemini lần 2 trong lượt thử này')); return fetch(u, i); }) as typeof fetch;
const khoa = Deno.env.get('GEMINI_API_KEY');
let gem = null;
if (khoa) {
  gem = await goiGemini(uv, khoa, fetchMotLan);
  d.push(gem.ok ? `Gemini THẬT: OK sau ${gem.so_lan} lần gọi, ${gem.muc.length} tin hợp lệ (bỏ ${gem.bo})` : `Gemini THẬT: LỖI (${gem.loai}) ${gem.ly_do} — số lần gọi thật: ${soGoi}`);
} else d.push('CHƯA kiểm Gemini thật: không có biến môi trường GEMINI_API_KEY trong phiên này.');
const nd = dungNoiDung(new Date(now + 7 * 3600000).toISOString().slice(0, 10), now, dungPhanDau([], [], now), uv, gem, lay.loi);
d.push(`Bản tin: ${nd.tin.length} tin, dung_ai=${nd.dung_ai}${nd.ly_do_khong_ai ? ' (' + nd.ly_do_khong_ai + ')' : ''}`);
const uvLink = new Set(uv.map((u) => u.link));
d.push(`Mọi link đều lấy từ RSS gốc: ${nd.tin.every((m) => uvLink.has(m.link))}`);
const khuc = dungVanBanTelegram(nd);
d.push(`Telegram sẽ gửi ${khuc.length} tin nhắn, độ dài: ${khuc.map((k) => k.length).join(', ')} (giới hạn 4096)`, '', '----- NỘI DUNG TELEGRAM (HTML) -----', ...khuc);
Deno.writeTextFileSync(new URL('../docs/bang-chung/2.9/chay-that-ban-tin.txt', import.meta.url), d.join('\n') + '\n');
console.log(d.join('\n'));
