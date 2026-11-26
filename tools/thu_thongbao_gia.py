"""Thử hộp "Thông báo trên điện thoại" (2.5b) trong Cài đặt, bằng Supabase GIẢ + Notification/PushManager/serviceWorker GIẢ.
Chạy: py -3.12 tools/thu_thongbao_gia.py [thu_muc_ra]   (mặc định docs/bang-chung/2.5b; KHÔNG dùng -I)"""
import os, sys, json
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'bang-chung', '2.5b')
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, 'thu-giao-dien.txt'), 'w', encoding='utf-8')
ok_all = True
def check(ten, cond):
    global ok_all; ok_all &= bool(cond)
    t = ('  ĐẠT  ' if cond else '  HỎNG ') + ten; print(t); LOG.write(t + '\n')

CATS = [dict(id='cv', ten='Công việc', mau='#1a73e8', thu_tu=1)]
FAKE = """
window.__DB={su_kien:[],y_tuong:[],push_dang_ky:[]};
window.supabase={createClient:()=>{
 const q=(t)=>{const o={f:[],op:'select',pl:null,
  select:()=>o,order:()=>o,is:(c,v)=>{o.f.push(r=>r[c]==v);return o},not:()=>o,
  eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, lt:()=>o,
  insert:(p)=>{o.op='insert';o.pl=p;return o}, update:()=>o, delete:()=>{o.op='delete';return o},
  upsert:(p,opt)=>{o.op='upsert';o.pl=p;o.opt=opt;return o},
  then:(res)=>{ if(t=='app_owner') return res({data:[{user_id:'u1'}],error:null});
   if(t=='loai_viec') return res({data:%s,error:null});
   const D=window.__DB[t];
   if(o.op=='upsert'){ if(window.__UPSERT_ERR) return res({data:null,error:{message:'permission denied'}}); window.__DB[t]=D.filter(r=>r.endpoint!==o.pl.endpoint).concat([o.pl]); return res({data:null,error:null}); }
   if(o.op=='delete'){ const m=D.filter(r=>o.f.every(f=>f(r))); window.__DB[t]=D.filter(r=>!m.includes(r)); return res({data:null,error:null}); }
   return res({data:JSON.parse(JSON.stringify(D.filter(r=>o.f.every(f=>f(r))))),error:null}); }};return o};
 const ch={on:()=>ch,subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{access_token:'TOKEN_GIA',user:{id:'u1',email:'thu@gia'}}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};
""" % json.dumps(CATS)

INIT = """
(() => { const T = %s;
  if (T.ios) { Object.defineProperty(navigator, 'userAgent', { get: () => 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148 Safari/604.1' }); }
  if (T.standalone) { Object.defineProperty(navigator, 'standalone', { get: () => true }); }
  if (T.noNotif) { delete window.Notification; }
  else { let perm = T.perm; window.Notification = { get permission() { return perm; }, requestPermission: async () => { perm = T.ask; return T.ask; } }; }
  if (T.noPM) { delete window.PushManager; } else { window.PushManager = function () {}; }
  let sub = T.haveSub ? { endpoint: 'https://push.example/abc', toJSON() { return { endpoint: this.endpoint, keys: { p256dh: 'P', auth: 'A' } }; }, unsubscribe: async () => { sub = null; return true; } } : null;
  const reg = { pushManager: { getSubscription: async () => sub, subscribe: async (o) => { window.__SUBOPT = { uvo: o.userVisibleOnly, keyLen: o.applicationServerKey.length };
    sub = { endpoint: 'https://push.example/abc', toJSON() { return { endpoint: this.endpoint, keys: { p256dh: 'P', auth: 'A' } }; }, unsubscribe: async () => { sub = null; return true; } }; return sub; } } };
  Object.defineProperty(navigator, 'serviceWorker', { value: { ready: Promise.resolve(reg), register: () => Promise.resolve(reg) }, configurable: true });
})();
"""
def mo(b, T, **kw):
    ctx = b.new_context(viewport=dict(width=390, height=760), device_scale_factor=2, **kw); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.add_init_script(INIT % json.dumps(T))
    pg.route('**/@supabase/supabase-js@2', lambda r: r.fulfill(body=FAKE, content_type='application/javascript'))
    pg.goto('file:///' + ROOT.replace('\\', '/') + '/index.html')
    pg.wait_for_selector('#app:not([hidden])')
    pg.click('#duoi a[data-p=cai]'); pg.wait_for_timeout(300)
    return ctx, pg, errs
def st(pg): return pg.locator('#hopTb').get_attribute('data-st')
def vis(pg): return [i for i in ('tbBat', 'tbTat', 'tbThu') if pg.locator('#' + i).is_visible()]
def shot(pg, n): pg.locator('#hopTb').screenshot(path=os.path.join(OUT, n))

with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    # 1 iPhone chưa cài vào màn hình chính
    ctx, pg, e = mo(b, dict(ios=True, perm='default', ask='granted'))
    check('iPhone chưa Thêm vào MH chính: báo rõ lý do, không có nút bật', st(pg) == 'chua-ho-tro' and 'Thêm vào màn hình chính' in pg.inner_text('#tbHuong') and vis(pg) == [])
    shot(pg, '1-iphone-chua-cai.png'); check('không lỗi JS', not e); ctx.close()
    # 2 không hỗ trợ
    ctx, pg, e = mo(b, dict(noNotif=True, noPM=True, perm='default', ask='granted'))
    check('Trình duyệt không hỗ trợ: báo chưa hỗ trợ', st(pg) == 'chua-ho-tro' and 'chưa hỗ trợ' in pg.inner_text('#tbTrang') and vis(pg) == [])
    shot(pg, '2-chua-ho-tro.png'); ctx.close()
    # 3 bị chặn
    ctx, pg, e = mo(b, dict(ios=True, standalone=True, perm='denied', ask='denied'))
    check('Đã chặn: hướng dẫn mở lại trong Cài đặt điện thoại', st(pg) == 'bi-chan' and 'Cài đặt' in pg.inner_text('#tbHuong') and vis(pg) == [])
    shot(pg, '3-bi-chan.png'); ctx.close()
    # 4 iPhone đã cài, chưa bật -> bật -> gửi thử -> tắt
    ctx, pg, e = mo(b, dict(ios=True, standalone=True, perm='default', ask='granted'))
    calls = []
    def route(r):
        calls.append(dict(auth=r.request.headers.get('authorization'), body=r.request.post_data))
        r.fulfill(status=200, content_type='application/json', headers={'access-control-allow-origin': '*'}, body=json.dumps(dict(thu=True, gui=1, chet=0, loi=[])))
    pg.route('**/functions/v1/nhac-viec', route)
    check('App đã cài, chưa bật: chỉ có nút "Bật thông báo"', st(pg) == 'chua-bat' and vis(pg) == ['tbBat'])
    shot(pg, '4-chua-bat.png')
    pg.click('#tbBat'); pg.wait_for_timeout(500)
    db = pg.evaluate('window.__DB.push_dang_ky')
    check('Bấm bật: ghi 1 dòng push_dang_ky (endpoint, p256dh, auth)', len(db) == 1 and db[0]['endpoint'] == 'https://push.example/abc' and db[0]['p256dh'] == 'P' and db[0]['auth'] == 'A')
    so = pg.evaluate('window.__SUBOPT')
    check('subscribe dùng userVisibleOnly + khoá công khai 65 byte', so['uvo'] is True and so['keyLen'] == 65)
    check('Trạng thái chuyển "Đã bật", có nút Tắt + Gửi thử', st(pg) == 'da-bat' and vis(pg) == ['tbTat', 'tbThu'])
    shot(pg, '5-da-bat.png')
    pg.click('#tbThu'); pg.wait_for_timeout(500)
    check('Gửi thử gọi function với token đăng nhập', len(calls) == 1 and calls[0]['auth'] == 'Bearer TOKEN_GIA' and '"thu":true' in calls[0]['body'])
    check('Có thông báo "Đã gửi thử"', 'Đã gửi thử' in pg.inner_text('#toast'))
    pg.screenshot(path=os.path.join(OUT, '6-gui-thu.png'))
    pg.click('#tbTat'); pg.wait_for_timeout(500)
    check('Bấm tắt: xoá dòng đăng ký + quay về "Chưa bật"', pg.evaluate('window.__DB.push_dang_ky') == [] and st(pg) == 'chua-bat')
    check('không lỗi JS', not e); ctx.close()
    # 5 từ chối quyền khi bấm
    ctx, pg, e = mo(b, dict(ios=True, standalone=True, perm='default', ask='denied'))
    pg.click('#tbBat'); pg.wait_for_timeout(400)
    check('Từ chối quyền: không ghi DB, chuyển "Bị chặn"', pg.evaluate('window.__DB.push_dang_ky') == [] and st(pg) == 'bi-chan'); ctx.close()
    # 6 chưa chạy SQL -> lỗi lưu
    ctx, pg, e = mo(b, dict(ios=True, standalone=True, perm='default', ask='granted'))
    pg.evaluate('window.__UPSERT_ERR = true'); pg.click('#tbBat'); pg.wait_for_timeout(500)
    check('Lưu đăng ký lỗi: báo nhắc chạy SQL, hoàn tác đăng ký, không hiện "Đã bật"', 'sql/2.5d-push.sql' in pg.inner_text('#toast') and st(pg) == 'chua-bat'); ctx.close()
    # 7 máy tính (không iOS) đã đăng ký sẵn
    ctx, pg, e = mo(b, dict(perm='granted', ask='granted', haveSub=True))
    check('Máy tính đã có đăng ký: hiện "Đã bật"', st(pg) == 'da-bat'); ctx.close()
    b.close()
LOG.write('KẾT QUẢ: ' + ('TẤT CẢ ĐẠT' if ok_all else 'CÓ LỖI') + '\n'); print('KẾT QUẢ:', 'TẤT CẢ ĐẠT' if ok_all else 'CÓ LỖI')
sys.exit(0 if ok_all else 1)
