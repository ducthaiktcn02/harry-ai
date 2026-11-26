// Chạy THẬT phần lấy tin (gọi RSS công khai thật, không khoá) bằng đúng mã của Edge Function ban-tin-lay.
// Chạy: deno run --allow-net --allow-write tools/chay_that_ban_tin.ts   -> docs/bang-chung/2.8/tin-tho.json + tin-tho.txt
import { HAN_CHOT_MS, NGUON } from '../supabase/functions/ban-tin-lay/nguon.ts';
import { layTatCa } from '../supabase/functions/ban-tin-lay/loi.ts';

async function tai(url: string): Promise<string> {
  let loi: unknown;
  for (let i = 0; i < 2; i++) {
    try {
      const r = await fetch(url, {
        signal: AbortSignal.timeout(HAN_CHOT_MS),
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; HarryAI-BanTin/1.0)', Accept: 'application/rss+xml, application/xml, text/xml, */*' },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.text();
    } catch (e) { loi = e; }
  }
  throw loi;
}

const t0 = Date.now();
const kq = await layTatCa(NGUON, tai, Date.now());
const giay = ((Date.now() - t0) / 1000).toFixed(1);
const out = new URL('../docs/bang-chung/2.8/', import.meta.url);
Deno.writeTextFileSync(new URL('tin-tho.json', out), JSON.stringify(kq, null, 1));
const d = [`Chạy thật lúc ${new Date().toISOString()} — mất ${giay}s cho ${NGUON.length} nguồn RSS`, `Tổng ${kq.dem.tong} tin (trước khi gộp ${kq.dem.truoc_khi_gop}, gộp trùng ${kq.dem.da_gop_trung}); nguồn OK ${kq.dem.nguon_ok}, lỗi ${kq.dem.nguon_loi}`, ''];
for (const [cd, ds] of Object.entries(kq.tin)) {
  d.push(`## ${cd}: ${ds.length} tin`);
  for (const t of ds.slice(0, 4)) d.push(`  - [${t.bao}] ${t.tieu_de} (${t.thoi_gian.slice(0, 16)}Z)${t.trung_voi ? ' | trùng với: ' + t.trung_voi.join(', ') : ''}\n      ${t.link}`);
}
d.push('', 'Theo báo: ' + Object.entries(kq.dem.theo_bao).map(([k, v]) => `${k}=${v}`).join(', '));
d.push('Nguồn lỗi (bỏ qua): ' + (kq.loi.length ? kq.loi.join('; ') : '(không có)'));
for (const l of kq.loi_chi_tiet) d.push(`  - ${l.bao} / ${l.chu_de}: ${l.ly_do} — ${l.url}`);
Deno.writeTextFileSync(new URL('tin-tho.txt', out), d.join('\n') + '\n');
console.log(d.join('\n'));
