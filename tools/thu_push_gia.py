"""Thử logic Edge Function nhac-viec (Telegram + Web Push) bằng đối tượng GIẢ, chạy trong Chrome (máy không có Deno/Node).
Bóc kiểu TypeScript bằng regex rồi chạy chính mã trong index.ts. Không gọi mạng thật.
Chạy: py -3.12 tools/thu_push_gia.py [thu_muc_ra]  (mặc định docs/bang-chung/2.5b; KHÔNG dùng -I)"""
import re, os, sys, json
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'bang-chung', '2.5b')
os.makedirs(OUT, exist_ok=True)
s = open(os.path.join(ROOT, 'supabase/functions/nhac-viec/index.ts'), encoding='utf-8').read()
s = re.sub(r"^import .*$", "", s, flags=re.M)
s = re.sub(r"type Row = \{.*?\};\n", "", s, flags=re.S)
s = s.replace("payload: { title: string; body: string; tag: string; url?: string }", "payload")
s = s.replace("(r: Row, from: number, to: number): number[]", "(r, from, to)")
s = s.replace("(sb: any", "(sb").replace("(d: any)", "(d)").replace("(e: any)", "(e)")
s = re.sub(r"\b(const|let) (\w+): (string\[\]|Response \| null|number\[\]) =", r"\1 \2 =", s)
s = s.replace("[] as string[]", "[]").replace(") as Row[]", ")")
s = s.replace("(t: number)", "(t)").replace("(o: unknown, status = 200)", "(o, status = 200)")
s = s.replace("(r: Row)", "(r)")
s = re.sub(r"\)!", ")", s)
s = re.sub(r"(\w)!(?=[,\.\)\s;])", r"\1", s)
s = s.replace("const ngay = (t: number)", "const ngay = (t)").replace("const gio = (t: number)", "const gio = (t)")

FAKE = r"""
window.__R = async function(cfg){
  const db = { su_kien: cfg.events, nhac_da_gui: cfg.daGui || [], push_dang_ky: cfg.subs.map((x,i)=>({id:'p'+i, endpoint:x, p256dh:'k', auth:'a'})) };
  const tele = [], pushes = []; let chet = [];
  const env = { CRON_KEY:'ck', TELEGRAM_BOT_TOKEN:'tok', TELEGRAM_CHAT_ID:'chat', SUPABASE_URL:'u', SUPABASE_SERVICE_ROLE_KEY:'s', SUPABASE_ANON_KEY:'a', VAPID_PUBLIC_KEY:'pub', VAPID_PRIVATE_KEY:'pri', ...(cfg.env||{}) };
  Object.keys(env).forEach(k => env[k]===null && delete env[k]);
  const Deno = { env:{ get:(k)=>env[k] }, serve:(h)=>{ window.__H = h; } };
  const webpush = { setVapidDetails(){}, async sendNotification(sub, body){
      const m = (cfg.pushMode||{})[sub.endpoint] || 'ok';
      if (m==='dead') throw {statusCode:410, message:'gone'};
      if (m==='boom') throw {statusCode:500, message:'loi'};
      pushes.push({ep:sub.endpoint, body:JSON.parse(body)}); } };
  const createClient = (u,k,o) => ({
    rpc: async()=>({data: cfg.laChu !== false, error:null}),
    from: (t) => { const o={f:[],op:'sel',pl:null,
      select:()=>o, is:(c,v)=>{o.f.push(r=>r[c]==v);return o}, not:(c,_,v)=>{o.f.push(r=>r[c]!=v);return o},
      eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, insert:(p)=>{o.op='ins';o.pl=p;return o}, delete:()=>{o.op='del';return o},
      then:(res)=>{ const D=db[t];
        if(o.op==='ins'){ if(D.some(r=>r.su_kien_id===o.pl.su_kien_id&&r.lan===o.pl.lan)) return res({error:{message:'dup'}}); D.push(o.pl); return res({error:null}); }
        if(o.op==='del'){ const m=D.filter(r=>o.f.every(f=>f(r))); if(t==='push_dang_ky') chet.push(...m.map(x=>x.endpoint)); db[t]=D.filter(r=>!m.includes(r)); return res({error:null}); }
        return res({data:D.filter(r=>o.f.every(f=>f(r))), error:null}); }}; return o; } });
  const fetch = async (url, init) => { tele.push(JSON.parse(init.body).text); if(cfg.tele==='throw') throw new Error('net'); return {ok: cfg.tele!=='500', status: cfg.tele==='500'?500:200}; };
  const code = __CODE__;
  new Function('Deno','webpush','createClient','fetch', code)(Deno, webpush, createClient, fetch);
  const hdr = cfg.headers || {'x-cron-key':'ck'};
  const resp = await window.__H({ method: cfg.method||'POST', headers:{ get:(k)=>hdr[k.toLowerCase()]||null } });
  const body = resp.status===200 ? await resp.json().catch(()=>null) : await resp.text();
  return { status: resp.status, body, tele, pushes, chet, daGui: db.nhac_da_gui.length, subsConLai: db.push_dang_ky.map(x=>x.endpoint) };
};
""".replace('__CODE__', json.dumps(s))

ok_all = True
LOG = open(os.path.join(OUT, 'thu-push-gia.txt'), 'w', encoding='utf-8')
def check(ten, cond, extra=''):
    global ok_all; ok_all &= bool(cond)
    t = ('  ĐẠT  ' if cond else '  HỎNG ') + ten + ((' ' + str(extra)) if (extra and not cond) else '')
    print(t); LOG.write(t + '\n')
def ev():
    return dict(id='e1', tieu_de='Họp nhóm', ghi_chu=None, ca_ngay=False, lap='none', lap_den=None, lap_ngoai=[], nhac_phut=0)
JS = "(c)=>{c.events.forEach(e=>{e.bat_dau=new Date(Date.now()-60000).toISOString();e.ket_thuc=e.bat_dau});" \
     "if(c.daGuiLanSuKien) c.daGui=[{su_kien_id:'e1',lan:c.events[0].bat_dau}]; return window.__R(c)}"
def run(pg, **cfg):
    cfg.setdefault('events', [ev()]); cfg.setdefault('subs', [])
    return pg.evaluate(JS, cfg)

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome'); pg = b.new_page(); pg.set_content('<html></html>'); pg.add_script_tag(content=FAKE)
    r = run(pg, subs=['A', 'B'])
    check('Gửi cả Telegram (1) lẫn push (2 thiết bị)', len(r['tele']) == 1 and len(r['pushes']) == 2 and r['body']['pushGui'] == 2, r)
    check('Nội dung push có tiêu đề + tag chống trùng', r['pushes'] and r['pushes'][0]['body']['title'].endswith('Họp nhóm') and r['pushes'][0]['body']['tag'].startswith('nhac-e1-'), r)
    r = run(pg, subs=['A', 'B'], pushMode={'B': 'dead'})
    check('Đăng ký chết (410) bị xoá, đăng ký sống còn', r['chet'] == ['B'] and r['subsConLai'] == ['A'] and r['body']['pushChet'] == 1, r)
    check('Có đăng ký chết vẫn gửi Telegram', len(r['tele']) == 1, r)
    r = run(pg, subs=['A'], pushMode={'A': 'boom'})
    check('Push lỗi 500: Telegram vẫn gửi, đăng ký không bị xoá', len(r['tele']) == 1 and r['subsConLai'] == ['A'] and r['body']['daGui'] == 1 and r['daGui'] == 1, r)
    r = run(pg, subs=['A'], env={'VAPID_PUBLIC_KEY': None, 'VAPID_PRIVATE_KEY': None})
    check('Thiếu secrets VAPID: Telegram vẫn gửi, báo lỗi rõ', len(r['tele']) == 1 and r['pushes'] == [] and any('VAPID' in x for x in r['body']['loi']), r)
    r = run(pg, subs=['A'], tele='500')
    check('Telegram lỗi nhưng push tới nơi: tính đã nhắc, không nhắc lại', r['daGui'] == 1 and len(r['pushes']) == 1, r)
    r = run(pg, subs=['A'], tele='500', pushMode={'A': 'boom'})
    check('Cả hai lỗi: xoá dấu để lần sau thử lại', r['daGui'] == 0, r)
    r = run(pg, subs=['A'], tele='throw')
    check('Telegram ném lỗi mạng: không sập, push vẫn đi', r['status'] == 200 and len(r['pushes']) == 1, r)
    r = run(pg, subs=['A'], daGuiLanSuKien=True)
    check('Đã nhắc rồi (nhac_da_gui) thì không gửi lại cả Telegram lẫn push', r['tele'] == [] and r['pushes'] == [], r)
    r = run(pg, subs=['A'], headers={})
    check('Không có khoá cron/đăng nhập -> 403, không gửi gì', r['status'] == 403 and r['tele'] == [] and r['pushes'] == [], r)
    r = run(pg, subs=['A', 'B'], headers={'authorization': 'Bearer tokNguoiDung'}, events=[])
    check('Gửi thử (chủ app): push tới mọi thiết bị, KHÔNG Telegram', r['status'] == 200 and len(r['pushes']) == 2 and r['tele'] == [] and r['body'].get('thu') is True, r)
    r = run(pg, subs=['A'], headers={'authorization': 'Bearer tokNguoiLa'}, laChu=False, events=[])
    check('Gửi thử bởi người không phải chủ -> 403, không push', r['status'] == 403 and r['pushes'] == [], r)
    r = run(pg, subs=['A'], method='OPTIONS', headers={})
    check('OPTIONS (CORS) trả 200', r['status'] == 200, r)
    b.close()
LOG.write('KẾT QUẢ: ' + ('TẤT CẢ ĐẠT' if ok_all else 'CÓ LỖI') + '\n'); print('KẾT QUẢ:', 'TẤT CẢ ĐẠT' if ok_all else 'CÓ LỖI')
sys.exit(0 if ok_all else 1)
