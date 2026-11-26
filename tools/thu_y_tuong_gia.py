"""Thử 2.6 (Kho ý tưởng) bằng Supabase GIẢ nhớ trong bộ nhớ.
Chạy: py -3.12 tools/thu_y_tuong_gia.py [thu_muc_ra]   (mặc định docs/bang-chung/2.6; KHÔNG dùng -I)"""
import os, sys, json, datetime as dt
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'bang-chung', '2.6')
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, 'thu-y-tuong.txt'), 'w', encoding='utf-8')
def say(*a):
    t = ' '.join(str(x) for x in a); print(t); LOG.write(t + '\n'); LOG.flush()

now = dt.datetime.now().astimezone()
def ago(days): return (now - dt.timedelta(days=days)).isoformat()
def y(i, ten, tt, uu, nhan, ghi=None, han=None, sua=0, tu=0):
    return dict(id=i, tieu_de=ten, ghi_chu=ghi, trang_thai=tt, uu_tien=uu, nhan=nhan, han=han, thu_tu=tu,
                tao_luc=ago(sua), sua_luc=ago(sua), xoa_luc=None, nguon=None, link=None)
YT = [y('y1', 'Làm kênh review đồ bếp', 'chua_lam', 'cao', ['video'], 'Quay thử 3 sản phẩm nồi chiên', sua=20, tu=1),
      y('y2', 'Mua micro mới', 'chua_lam', 'vua', ['thiết bị'], sua=2, tu=2),
      y('y3', 'Dựng video kem Acne', 'dang_lam', 'cao', ['video'], han=(now + dt.timedelta(days=3)).strftime('%Y-%m-%d'), sua=1, tu=3),
      y('y4', 'Học Excel cơ bản', 'xong', 'thap', ['học'], sua=5, tu=4)]
SK = [dict(id='e1', tieu_de='Họp cũ', ghi_chu=None, bat_dau=ago(40), ket_thuc=ago(40), ca_ngay=False, loai='cv', xoa_luc=ago(3), lap='none', lap_den=None, lap_ngoai=[])]
CATS = [dict(id='cv', ten='Công việc', mau='#1a73e8', thu_tu=1)]
FAKE = """
window.__DB={su_kien:%s,y_tuong:%s}; window.__RT={}; let __n=100;
const DEF={y_tuong:()=>({ghi_chu:null,trang_thai:'chua_lam',uu_tien:'vua',nhan:[],han:null,thu_tu:0,tao_luc:new Date().toISOString(),sua_luc:new Date().toISOString(),xoa_luc:null,nguon:null,link:null}),
 su_kien:()=>({xoa_luc:null,lap:'none',lap_den:null,lap_ngoai:[],ghi_chu:null})};
window.supabase={createClient:()=>{
 const q=(t)=>{const o={f:[],op:'select',pl:null,ord:null,
  select:()=>o,order:(c)=>{o.ord=c;return o},
  is:(c,v)=>{o.f.push(r=>r[c]==v);return o}, not:(c,_,v)=>{o.f.push(r=>r[c]!=v);return o},
  eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, lt:(c,v)=>{o.f.push(r=>r[c]!=null&&r[c]<v);return o},
  insert:(p)=>{o.op='insert';o.pl=p;return o}, update:(p)=>{o.op='update';o.pl=p;return o}, delete:()=>{o.op='delete';return o},
  then:(res)=>{ if(t=='app_owner') return res({data:[{user_id:'u1'}],error:null});
   if(t=='loai_viec') return res({data:%s,error:null});
   const D=window.__DB[t]; const m=D.filter(r=>o.f.every(f=>f(r)));
   if(o.op=='insert'){const rows=[].concat(o.pl).map(p=>({id:'n'+(++__n),...DEF[t](),...p}));rows.forEach(r=>D.push(r));return res({data:null,error:null});}
   if(o.op=='update'){m.forEach(r=>Object.assign(r,o.pl));return res({data:null,error:null});}
   if(o.op=='delete'){window.__DB[t]=D.filter(r=>!m.includes(r));return res({data:null,error:null});}
   const out=JSON.parse(JSON.stringify(m)); if(o.ord) out.sort((a,b)=>(a[o.ord]>b[o.ord])-(a[o.ord]<b[o.ord]));
   return res({data:out,error:null}); }};return o};
 const ch={on:(_,f,cb)=>{window.__RT[f.table]=cb;return ch},subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'thu@gia'}}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};
""" % (json.dumps(SK), json.dumps(YT), json.dumps(CATS))

ok_all = True
def check(ten, cond):
    global ok_all
    ok_all &= bool(cond); say(('  ĐẠT  ' if cond else '  HỎNG '), ten)
def tbl(pg, t): return pg.evaluate("t=>window.__DB[t]", t)
def yy(pg, i): return [r for r in tbl(pg, 'y_tuong') if r['id'] == i][0]
def shot(pg, name): pg.screenshot(path=os.path.join(OUT, name))
def lane(pg, k): return pg.locator(f".lane[data-s={k}]")
def keo_chuot(pg, card, k):
    bb = card.bounding_box(); lb = lane(pg, k).bounding_box()
    pg.mouse.move(bb['x'] + 20, bb['y'] + 10); pg.mouse.down()
    pg.mouse.move(bb['x'] + 40, bb['y'] + 30, steps=4)
    pg.mouse.move(lb['x'] + lb['width'] / 2, lb['y'] + 60, steps=8)
    return lambda: (pg.mouse.up(), pg.wait_for_timeout(400))

def mo(browser, **kw):
    ctx = browser.new_context(**kw); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=FAKE, content_type="application/javascript"))
    pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
    pg.wait_for_selector("#app:not([hidden])")
    return ctx, pg, errs

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx, pg, errs = mo(b, viewport=dict(width=1200, height=800))
    pg.click(".nav a[data-p=y]"); pg.wait_for_timeout(300)
    pg.select_option("#fUu", "")  # mặc định

    say("1) Bảng 3 cột + cảnh báo để lâu")
    check("3 cột Chưa làm / Đang làm / Đã xong", pg.locator(".lane").count() == 3)
    check("Chưa làm có 2 thẻ, Đang làm 1, Đã xong 1", lane(pg, 'chua_lam').locator('.card').count() == 2 and lane(pg, 'dang_lam').locator('.card').count() == 1 and lane(pg, 'xong').locator('.card').count() == 1)
    check("Thẻ 'Làm kênh review' (20 ngày) có cảnh báo để lâu", pg.locator(".card:has-text('review đồ bếp') .old").count() == 1)
    check("Thẻ 'Mua micro' (2 ngày) KHÔNG cảnh báo", pg.locator(".card:has-text('Mua micro') .old").count() == 0)
    check("Thẻ Đang làm quá lâu cũng không cảnh báo (chỉ Chưa làm)", pg.locator(".lane[data-s=dang_lam] .old").count() == 0)
    shot(pg, "01-bang-may-tinh.png")

    say("2) Thêm ý tưởng")
    pg.click("#bYMoi"); pg.fill("#yTen", "Quay video unbox máy xay"); pg.fill("#yGhi", "Góc quay từ trên xuống")
    pg.select_option("#yUu", "cao"); pg.fill("#yNhan", "video, #bếp, video"); pg.fill("#yHan", "2026-12-20")
    shot(pg, "02-hop-thoai-them-may-tinh.png")
    pg.click("#yLuu"); pg.wait_for_timeout(400)
    n = [r for r in tbl(pg, 'y_tuong') if r['tieu_de'] == 'Quay video unbox máy xay']
    check("Lưu vào bảng: ưu tiên cao, nhãn [video, bếp] (bỏ #, bỏ trùng), hạn 2026-12-20", len(n) == 1 and n[0]['uu_tien'] == 'cao' and n[0]['nhan'] == ['video', 'bếp'] and n[0]['han'] == '2026-12-20' and n[0]['trang_thai'] == 'chua_lam')
    check("Thẻ mới hiện ở đầu cột Chưa làm", lane(pg, 'chua_lam').locator('.card').first.inner_text().startswith('Quay video unbox'))
    pg.click("#bYMoi"); pg.click("#yLuu"); pg.wait_for_timeout(200)
    check("Thiếu tiêu đề thì không lưu", len(tbl(pg, 'y_tuong')) == 5)
    pg.click("#yHuy")

    say("3) Sửa ý tưởng")
    pg.locator(".card:has-text('Mua micro')").click(); pg.wait_for_timeout(200)
    pg.fill("#yTen", "Mua micro không dây"); pg.select_option("#yUu", "thap"); pg.click("#yLuu"); pg.wait_for_timeout(400)
    m = yy(pg, 'y2')
    check("Đã sửa tiêu đề + ưu tiên thấp", m['tieu_de'] == 'Mua micro không dây' and m['uu_tien'] == 'thap')
    check("Sửa xong, thẻ hiện tên mới trong bảng", pg.locator(".card:has-text('Mua micro không dây')").count() == 1)

    say("4) Kéo thả bằng chuột đổi trạng thái")
    xong = keo_chuot(pg, pg.locator(".card:has-text('review đồ bếp')"), 'dang_lam')
    check("Cột đích sáng lên khi kéo qua", pg.locator(".lane.drop[data-s=dang_lam]").count() == 1)
    shot(pg, "03-dang-keo.png")
    xong()
    r = yy(pg, 'y1')
    check("Kéo sang Đang làm -> trang_thai = dang_lam", r['trang_thai'] == 'dang_lam')
    check("Kéo xong thì hết 'để lâu' (sua_luc mới)", pg.locator(".card:has-text('review đồ bếp') .old").count() == 0)
    check("Thẻ nằm đầu cột Đang làm", lane(pg, 'dang_lam').locator('.card').first.inner_text().startswith('Làm kênh review'))
    keo_chuot(pg, pg.locator(".card:has-text('Mua micro')"), 'xong')()
    check("Kéo sang Đã xong", yy(pg, 'y2')['trang_thai'] == 'xong')
    keo_chuot(pg, pg.locator(".card:has-text('Mua micro')"), 'xong')()
    check("Thả lại đúng cột cũ: không đổi gì và không mở hộp thoại", pg.locator("#ov.on").count() == 0)
    pg.wait_for_timeout(600)  # sau khi kéo, app bỏ qua cú bấm trong 0,5s (tránh mở nhầm)
    pg.click(".card:has-text('Học Excel')"); pg.wait_for_timeout(200)
    check("Bấm (không kéo) vào thẻ mở hộp thoại sửa", pg.locator("#ov.on #yTen").count() == 1)
    pg.click("#yHuy")

    say("5) Lọc ưu tiên và nhãn")
    shot(pg, "04-bang-sau-keo.png")
    pg.select_option("#fUu", "cao"); pg.wait_for_timeout(200)
    check("Lọc ưu tiên Cao: chỉ thẻ ưu tiên cao", pg.locator(".card").count() == 3 and pg.locator(".card .pri-cao").count() == 3)
    shot(pg, "05-loc-uu-tien-cao.png")
    pg.select_option("#fNhan", "bếp"); pg.wait_for_timeout(200)
    check("Thêm lọc nhãn 'bếp': còn 1 thẻ", pg.locator(".card").count() == 1 and pg.locator(".card:has-text('unbox')").count() == 1)
    pg.select_option("#fUu", ""); pg.select_option("#fNhan", "video"); pg.wait_for_timeout(200)
    check("Lọc nhãn 'video' (mọi ưu tiên): 3 thẻ", pg.locator(".card").count() == 3)
    pg.select_option("#fNhan", ""); pg.wait_for_timeout(200)
    check("Bỏ lọc: đủ 5 thẻ", pg.locator(".card").count() == 5)

    say("6) Dạng danh sách")
    pg.click("#bDs"); pg.wait_for_timeout(200)
    check("Danh sách có 5 dòng", pg.locator("tr.dong").count() == 5)
    check("Danh sách ghi trạng thái tiếng Việt", pg.locator("tr.dong:has-text('Học Excel'):has-text('Đã xong')").count() == 1)
    shot(pg, "06-danh-sach-may-tinh.png")
    pg.locator("tr.dong:has-text('Học Excel')").click(); pg.wait_for_timeout(200)
    check("Bấm dòng mở hộp thoại sửa", pg.locator("#yTen").count() == 1 and pg.input_value("#yTen") == "Học Excel cơ bản")
    pg.click("#yHuy"); pg.click("#bBang"); pg.wait_for_timeout(200)

    say("7) Xoá -> thùng rác dùng chung -> khôi phục")
    pg.locator(".card:has-text('Học Excel')").click(); pg.wait_for_timeout(200)
    pg.click("#yXoa"); pg.wait_for_timeout(400)
    check("Thẻ biến mất khỏi bảng, có xoa_luc", pg.locator(".card:has-text('Học Excel')").count() == 0 and yy(pg, 'y4')['xoa_luc'])
    pg.click("#btnCai"); pg.click("#btnRac"); pg.wait_for_timeout(300)
    check("Thùng rác có ý tưởng 💡 và cả sự kiện cũ", pg.locator(".dong-rac:has-text('Học Excel')").count() == 1 and pg.locator(".dong-rac:has-text('Họp cũ')").count() == 1)
    shot(pg, "07-thung-rac.png")
    pg.click(".dong-rac:has-text('Học Excel') [data-kp]"); pg.wait_for_timeout(400)
    check("Khôi phục: rời thùng rác (sự kiện vẫn còn)", pg.locator(".dong-rac:has-text('Học Excel')").count() == 0 and pg.locator(".dong-rac:has-text('Họp cũ')").count() == 1)
    pg.click(".nav a[data-p=y]"); pg.wait_for_timeout(300)
    check("Ý tưởng trở lại cột Đã xong", lane(pg, 'xong').locator(".card:has-text('Học Excel')").count() == 1)

    say("8) Xoá hẳn + tự dọn sau 30 ngày")
    pg.locator(".card:has-text('unbox')").click(); pg.wait_for_timeout(200); pg.click("#yXoa"); pg.wait_for_timeout(300)
    pg.click(".nav a[data-p=rac]"); pg.wait_for_timeout(300)
    pg.click(".dong-rac:has-text('unbox') [data-xh]"); pg.wait_for_timeout(300)
    check("Xoá hẳn: mất khỏi bảng dữ liệu", not [r for r in tbl(pg, 'y_tuong') if 'unbox' in r['tieu_de']])
    pg.evaluate("window.__DB.y_tuong.push({id:'cu',tieu_de:'Ý tưởng đã xoá 31 ngày',ghi_chu:null,trang_thai:'chua_lam',uu_tien:'vua',nhan:[],han:null,thu_tu:0,tao_luc:new Date().toISOString(),sua_luc:new Date().toISOString(),xoa_luc:new Date(Date.now()-31*864e5).toISOString(),nguon:null,link:null})")
    pg.reload(); pg.wait_for_selector("#app:not([hidden])"); pg.wait_for_timeout(500)
    check("Mở lại app: ý tưởng xoá > 30 ngày bị dọn", not [r for r in tbl(pg, 'y_tuong') if r['id'] == 'cu'])

    say("9) Đồng bộ tức thì (giả lập tin báo thay đổi từ thiết bị khác)")
    pg.click(".nav a[data-p=y]"); pg.wait_for_timeout(300)
    pg.evaluate("window.__DB.y_tuong.push({id:'tb',tieu_de:'Thêm từ máy khác',ghi_chu:null,trang_thai:'dang_lam',uu_tien:'vua',nhan:[],han:null,thu_tu:-9,tao_luc:new Date().toISOString(),sua_luc:new Date().toISOString(),xoa_luc:null,nguon:null,link:null}); window.__RT.y_tuong()")
    pg.wait_for_timeout(500)
    check("Thẻ từ thiết bị khác hiện ra không cần tải lại", pg.locator(".card:has-text('Thêm từ máy khác')").count() == 1)
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS: %s' % errs, not errs)
    ctx.close()

    say("10) Điện thoại (390x800, cảm ứng): bảng, danh sách, nhấn giữ rồi kéo")
    ctx, pg, errs = mo(b, viewport=dict(width=390, height=800), has_touch=True, is_mobile=True, device_scale_factor=2)
    check("Có thanh menu dưới (Lịch / Ý tưởng / Bản tin / Cài đặt)", pg.locator("#duoi a").count() == 4)
    pg.click("#duoi a[data-p=y]"); pg.wait_for_timeout(300)
    check("Mở được Kho ý tưởng từ thanh dưới", pg.locator("#p-y.on").count() == 1)
    shot(pg, "08-bang-dien-thoai.png")
    cdp = ctx.new_cdp_session(pg)
    def touch(typ, x, yv): cdp.send("Input.dispatchTouchEvent", dict(type=typ, touchPoints=[] if typ == 'touchEnd' else [dict(x=x, y=yv)]))
    card = pg.locator(".card:has-text('Mua micro')"); cb = card.bounding_box(); lb = lane(pg, 'dang_lam').bounding_box()
    cx, cy = cb['x'] + 20, cb['y'] + 10
    # kéo NGAY (không nhấn giữ): phải coi là cuộn, KHÔNG đổi trạng thái
    touch('touchStart', cx, cy); touch('touchMove', cx + 40, cy + 20); pg.wait_for_timeout(50)
    touch('touchMove', lb['x'] + 30, lb['y'] + 60); touch('touchEnd', 0, 0); pg.wait_for_timeout(500)
    check("Kéo ngay không nhấn giữ: không đổi trạng thái (để cuộn trang)", yy(pg, 'y2')['trang_thai'] == 'chua_lam')
    # nhấn giữ 0,5s rồi kéo sang Đang làm
    cb = card.bounding_box(); cx, cy = cb['x'] + 20, cb['y'] + 10
    touch('touchStart', cx, cy); pg.wait_for_timeout(500)
    touch('touchMove', cx + 20, cy + 10)
    for k in range(1, 7): touch('touchMove', cx + (lb['x'] + 30 - cx) * k / 6, cy + (lb['y'] + 60 - cy) * k / 6)
    check("Đang giữ: thẻ nổi lên (.keo)", pg.locator(".card.keo").count() == 1)
    shot(pg, "09-dien-thoai-dang-keo.png")
    touch('touchEnd', 0, 0); pg.wait_for_timeout(500)
    check("Nhấn giữ rồi kéo sang Đang làm -> đổi trạng thái", yy(pg, 'y2')['trang_thai'] == 'dang_lam')
    pg.click("#bDs"); pg.wait_for_timeout(300)
    shot(pg, "10-danh-sach-dien-thoai.png")
    check("Danh sách trên điện thoại hiện đủ dòng", pg.locator("tr.dong").count() == 4)
    pg.tap("#fab"); pg.wait_for_timeout(300)
    check("Nút + trong trang Ý tưởng mở hộp thoại ý tưởng mới", pg.locator("#yTen").count() == 1)
    shot(pg, "11-hop-thoai-dien-thoai.png")
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS (điện thoại): %s' % errs, not errs)
    ctx.close(); b.close()
say("TẤT CẢ ĐẠT" if ok_all else "CÓ LỖI")
sys.exit(0 if ok_all else 1)
