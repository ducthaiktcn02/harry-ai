"""Thử 2.4 (kéo thả, lặp lại, thùng rác) bằng Supabase GIẢ nhớ trong bộ nhớ. Chạy: py -3.12 tools/thu_lap_gia.py <thu_muc_anh>"""
import os, sys, json, datetime as dt
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
now = dt.datetime.now().astimezone()
mon = (now - dt.timedelta(days=now.weekday())).replace(hour=0, minute=0, second=0, microsecond=0)
def at(d, h, m=0): return (mon + dt.timedelta(days=d)).replace(hour=h, minute=m).isoformat()
def row(i, ten, s, e, loai='cv', lap='none', den=None):
    return dict(id=i, tieu_de=ten, ghi_chu=None, bat_dau=s, ket_thuc=e, ca_ngay=False, loai=loai, xoa_luc=None, lap=lap, lap_den=den, lap_ngoai=[])
EVS = [row('a', 'Họp khách', at(1, 15), at(1, 16)),
       row('b', 'Họp tuần', at(0, 9), at(0, 10), 'vd', 'week'),
       row('c', 'Uống thuốc', at(0, 7), at(0, 7, 30), 'cn', 'day'),
       row('d', 'Trả tiền nhà', at(2, 11), at(2, 12), 'gd', 'month')]
CATS = [dict(id='cv',ten='Công việc',mau='#1a73e8',thu_tu=1),dict(id='vd',ten='Quay/làm video',mau='#d50000',thu_tu=2),dict(id='cn',ten='Cá nhân/sức khoẻ',mau='#0b8043',thu_tu=3),dict(id='gd',ten='Gia đình',mau='#f4511e',thu_tu=4)]
FAKE = """
window.__DB=%s; let __n=100;
window.supabase={createClient:()=>{
 const q=(t)=>{const o={f:[],op:'select',pl:null,
  select:()=>o,order:()=>o,
  is:(c,v)=>{o.f.push(r=>r[c]==v);return o}, not:(c,_,v)=>{o.f.push(r=>r[c]!=v);return o},
  eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, lt:(c,v)=>{o.f.push(r=>r[c]!=null&&r[c]<v);return o},
  insert:(p)=>{o.op='insert';o.pl=p;return o}, update:(p)=>{o.op='update';o.pl=p;return o}, delete:()=>{o.op='delete';return o},
  then:(res)=>{ if(t=='app_owner') return res({data:[{user_id:'u1'}],error:null});
   if(t=='loai_viec') return res({data:%s,error:null});
   const D=window.__DB; const m=D.filter(r=>o.f.every(f=>f(r)));
   if(o.op=='insert'){D.push({id:'n'+(++__n),xoa_luc:null,lap:'none',lap_den:null,lap_ngoai:[],ghi_chu:null,...o.pl});return res({data:null,error:null});}
   if(o.op=='update'){m.forEach(r=>Object.assign(r,o.pl));return res({data:null,error:null});}
   if(o.op=='delete'){window.__DB=D.filter(r=>!m.includes(r));return res({data:null,error:null});}
   return res({data:JSON.parse(JSON.stringify(m)),error:null}); }};return o};
 const ch={on:()=>ch,subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'thu@gia'}}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};
""" % (json.dumps(EVS), json.dumps(CATS))

def dbrows(pg): return pg.evaluate("window.__DB")
ok_all = True
def check(ten, cond):
    global ok_all
    ok_all &= bool(cond); print(('  ĐẠT  ' if cond else '  HỎNG '), ten)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport=dict(width=1200, height=900))
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=FAKE, content_type="application/javascript"))
    pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
    pg.wait_for_selector("#app:not([hidden])"); pg.select_option("#chonKieu", "week"); pg.wait_for_timeout(400)
    pg.evaluate("document.getElementById('lich').scrollTop=0"); pg.wait_for_timeout(100)

    print("1) Lặp lại hiện đúng ngày")
    check("Họp tuần ↻ 1 lần trong tuần", pg.locator(".ev:has-text('Họp tuần')").count() == 1)
    check("Uống thuốc lặp hằng ngày = 7 lần/tuần", pg.locator(".ev:has-text('Uống thuốc')").count() == 7)
    check("Trả tiền nhà (tháng) 1 lần", pg.locator(".ev:has-text('Trả tiền nhà')").count() == 1)
    pg.screenshot(path=os.path.join(OUT, "01-tuan-co-lap.png"))
    pg.click("#btnSau"); pg.wait_for_timeout(300)
    check("Tuần sau: Họp tuần vẫn hiện", pg.locator(".ev:has-text('Họp tuần')").count() == 1)
    check("Tuần sau: Trả tiền nhà (tháng) KHÔNG hiện", pg.locator(".ev:has-text('Trả tiền nhà')").count() == 0)
    pg.screenshot(path=os.path.join(OUT, "02-tuan-sau.png"))
    pg.click("#btnNay"); pg.wait_for_timeout(300)
    pg.evaluate("document.getElementById('lich').scrollTop=0")

    print("2) Kéo thả sự kiện thường (Họp khách 15:00 -> 17:00, sang ngày kế)")
    ev = pg.locator(".ev:has-text('Họp khách')").first; bb = ev.bounding_box()
    pg.mouse.move(bb['x'] + 10, bb['y'] + 8); pg.mouse.down()
    pg.mouse.move(bb['x'] + 60, bb['y'] + 60, steps=5)
    pg.mouse.move(bb['x'] + 10 + bb['width'], bb['y'] + 8 + 96, steps=8)
    pg.screenshot(path=os.path.join(OUT, "03-dang-keo.png"))
    pg.mouse.up(); pg.wait_for_timeout(400)
    a = [r for r in dbrows(pg) if r['id'] == 'a'][0]
    s = dt.datetime.fromisoformat(a['bat_dau']).astimezone()
    check("Giờ mới 17:00 (thực tế %s)" % s.strftime('%a %H:%M'), s.hour == 17 and s.minute == 0 and s.weekday() == 2)
    check("Giờ kết thúc giữ độ dài 1 giờ", dt.datetime.fromisoformat(a['ket_thuc']).astimezone().hour == 18)

    print("3) Kéo 1 lần của sự kiện lặp -> hỏi 3 lựa chọn -> 'Chỉ sự kiện này'")
    ev = pg.locator(".ev:has-text('Họp tuần')").first; bb = ev.bounding_box()
    pg.mouse.move(bb['x'] + 10, bb['y'] + 8); pg.mouse.down(); pg.mouse.move(bb['x'] + 12, bb['y'] + 40, steps=6)
    pg.mouse.move(bb['x'] + 12, bb['y'] + 8 + 96, steps=6); pg.mouse.up(); pg.wait_for_timeout(300)
    check("Hộp thoại có đủ 3 lựa chọn", pg.locator("input[name=pham]").count() == 3)
    pg.screenshot(path=os.path.join(OUT, "04-hoi-3-lua-chon.png"))
    pg.click("#pOk"); pg.wait_for_timeout(400)
    D = dbrows(pg); bm = [r for r in D if r['id'] == 'b'][0]
    check("Gốc ghi 1 ngoại lệ", len(bm['lap_ngoai']) == 1)
    nu = [r for r in D if r['tieu_de'] == 'Họp tuần' and r['id'] != 'b']
    check("Có 1 sự kiện lẻ mới lúc 11:00", len(nu) == 1 and dt.datetime.fromisoformat(nu[0]['bat_dau']).astimezone().hour == 11 and nu[0]['lap'] == 'none')
    check("Trong tuần vẫn đúng 1 'Họp tuần' lặp + 1 lẻ", pg.locator(".ev:has-text('Họp tuần')").count() == 1)

    print("4) Xoá 'Uống thuốc' từ thứ 4 trở đi")
    pg.locator(".ev:has-text('Uống thuốc')").nth(2).click(); pg.wait_for_timeout(200)
    pg.click("#bXoa"); pg.wait_for_timeout(200)
    pg.check("input[name=pham][value=fut]"); pg.click("#pOk"); pg.wait_for_timeout(400)
    check("Còn 2 lần Uống thuốc (T2, T3)", pg.locator(".ev:has-text('Uống thuốc')").count() == 2)
    check("Phần đã xoá nằm trong thùng rác (xoa_luc)", any(r['tieu_de'] == 'Uống thuốc' and r['xoa_luc'] for r in dbrows(pg)))
    pg.screenshot(path=os.path.join(OUT, "05-sau-khi-xoa-tu-T4.png"))

    print("5) Xoá sự kiện thường -> thùng rác -> khôi phục")
    pg.locator(".ev:has-text('Họp khách')").first.click(); pg.wait_for_timeout(200)
    pg.click("#bXoa"); pg.wait_for_timeout(400)
    check("Họp khách biến mất khỏi lịch", pg.locator(".ev:has-text('Họp khách')").count() == 0)
    pg.click("#btnCai"); pg.click("#btnRac"); pg.wait_for_timeout(300)
    check("Có trong thùng rác", pg.locator(".dong-rac:has-text('Họp khách')").count() == 1)
    pg.screenshot(path=os.path.join(OUT, "06-thung-rac.png"))
    pg.click(".dong-rac:has-text('Họp khách') [data-kp]"); pg.wait_for_timeout(300)
    check('Khôi phục: Họp khách rời thùng rác, Uống thuốc còn', pg.locator(".dong-rac:has-text('Họp khách')").count() == 0 and pg.locator(".dong-rac:has-text('Uống thuốc')").count() == 1)
    pg.click(".nav a[data-p=lich]"); pg.wait_for_timeout(300)
    check("Họp khách trở lại lịch", pg.locator(".ev:has-text('Họp khách')").count() == 1)

    print("6) Tạo sự kiện lặp mới từ hộp thoại")
    pg.click("#btnTao"); pg.fill("#fTen", "Tập gym"); pg.select_option("#fLap", "week"); pg.click("#bLuu"); pg.wait_for_timeout(400)
    n = [r for r in dbrows(pg) if r['tieu_de'] == 'Tập gym']
    check("Lưu được lặp hằng tuần", len(n) == 1 and n[0]['lap'] == 'week')
    pg.screenshot(path=os.path.join(OUT, "07-tao-lap.png"))
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS: %s' % errs, not errs)
    b.close()
print("TẤT CẢ ĐẠT" if ok_all else "CÓ LỖI")
sys.exit(0 if ok_all else 1)
