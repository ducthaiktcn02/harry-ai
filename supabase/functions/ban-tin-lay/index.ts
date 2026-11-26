// Edge Function "ban-tin-lay" (giai đoạn 2.8): tải RSS các báo đã chốt (nguon.ts) -> danh sách tin THÔ theo 7 chủ đề.
// Chưa dịch/tóm tắt/gửi Telegram (đó là 2.9). Không dùng khoá nào bên ngoài (RSS công khai).
// Quyền gọi: (a) chủ app đã đăng nhập (token + public.la_chu_app(), như "Gửi thử" của nhac-viec), hoặc (b) header x-cron-key = secret CRON_KEY.
// Deploy: tắt "Verify JWT" (function tự kiểm quyền). SUPABASE_URL / SUPABASE_ANON_KEY có sẵn tự động.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';
import { HAN_CHOT_MS, NGUON } from './nguon.ts';
import { layTatCa } from './loi.ts';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-cron-key',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', ...CORS } });

async function taiMotNguon(url: string): Promise<string> {
  // thử tối đa 2 lần (vài báo đôi khi cắt kết nối giữa chừng); mỗi lần có hạn chót riêng, tổng vẫn bị layTatCa chặn ở HAN_CHOT_MS
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

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  const cron = req.headers.get('x-cron-key');
  if (cron) {
    const khoa = Deno.env.get('CRON_KEY');
    if (!khoa || cron !== khoa) return new Response('forbidden', { status: 403 });
  } else {
    const auth = req.headers.get('authorization') || '';
    if (!auth.startsWith('Bearer ')) return json({ loi: 'Cần đăng nhập' }, 401);
    const nguoi = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
    const { data: chu, error } = await nguoi.rpc('la_chu_app');
    if (error || chu !== true) return json({ loi: 'Chỉ chủ app được lấy tin' }, 403);
  }
  try {
    const kq = await layTatCa(NGUON, taiMotNguon, Date.now());
    return json(kq);
  } catch (e) {
    return json({ loi: 'Không lấy được tin: ' + (e instanceof Error ? e.message : String(e)) }, 500);
  }
});
