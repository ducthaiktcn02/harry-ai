"""Thử vuốt lịch kiểu Google Calendar (cảm ứng thật qua CDP). Chạy: py -3.12 tools/thu_vuot_gia.py <thu_muc_anh>"""
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
   if(t=='y_tuong') return res({data:[],error:null});  // 2.6: kho ý tưởng rỗng, không liên quan phép thử này
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


def vuot(cdp, x0, y0, x1, y1, buoc=8, ms=160):
    t = lambda ty, x, y: cdp.send("Input.dispatchTouchEvent", {"type": ty, "touchPoints": ([{"x": x, "y": y}] if ty != "touchEnd" else [])})
    t("touchStart", x0, y0)
    for i in range(1, buoc + 1):
        t("touchMove", x0 + (x1 - x0) * i / buoc, y0 + (y1 - y0) * i / buoc); time_sleep(ms / 1000 / buoc)
    t("touchEnd", x1, y1)
import time
time_sleep = time.sleep
tieude = lambda pg: pg.inner_text("#tieude")

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport=dict(width=390, height=800), has_touch=True, is_mobile=True)
    pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=FAKE, content_type="application/javascript"))
    pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
    pg.wait_for_selector("#app:not([hidden])")
    cdp = ctx.new_cdp_session(pg)

    print("1) Tuần: vuốt ngang")
    pg.select_option("#chonKieu", "week"); pg.wait_for_timeout(300)
    a = pg.inner_text(".dau")
    vuot(cdp, 300, 400, 80, 410); pg.wait_for_timeout(500)
    b1 = pg.inner_text(".dau")
    check("Vuốt trái -> sang tuần sau (T2 đổi +7 ngày)", a != b1)
    vuot(cdp, 80, 400, 300, 410); pg.wait_for_timeout(500)
    check("Vuốt phải -> quay lại tuần trước", pg.inner_text(".dau") == a)
    pg.screenshot(path=os.path.join(OUT, "v1-tuan.png"))
    vuot(cdp, 200, 400, 235, 405); pg.wait_for_timeout(450)
    check("Vuốt ngắn/chậm (35px) -> KHÔNG đổi tuần", pg.inner_text(".dau") == a)

    print("2) Tuần: vuốt dọc = cuộn giờ, không đổi tuần")
    s0 = pg.evaluate("document.getElementById('lich').scrollTop")
    vuot(cdp, 200, 300, 200, 600); pg.wait_for_timeout(500)
    check("Vuốt dọc không đổi tuần", pg.inner_text(".dau") == a)
    check("Vuốt dọc cuộn giờ", pg.evaluate("document.getElementById('lich').scrollTop") != s0)

    print("3) Ngày: vuốt ngang")
    pg.select_option("#chonKieu", "day"); pg.wait_for_timeout(300)
    t0 = tieude(pg)
    vuot(cdp, 300, 400, 80, 400); pg.wait_for_timeout(500)
    check("Ngày: vuốt trái -> ngày sau", tieude(pg) != t0)
    vuot(cdp, 80, 400, 300, 400); pg.wait_for_timeout(500)
    check("Ngày: vuốt phải -> quay lại", tieude(pg) == t0)

    print("4) Tháng: vuốt dọc và ngang")
    pg.select_option("#chonKieu", "month"); pg.wait_for_timeout(300)
    m0 = tieude(pg)
    check("Tháng vừa khung, không cuộn", pg.evaluate("(()=>{const e=document.getElementById('lich');return e.scrollHeight<=e.clientHeight+2})()"))
    vuot(cdp, 200, 600, 200, 250); pg.wait_for_timeout(500)
    m1 = tieude(pg); check(f"Vuốt lên -> tháng sau ({m0} -> {m1})", m1 != m0)
    pg.screenshot(path=os.path.join(OUT, "v2-thang.png"))
    vuot(cdp, 200, 250, 200, 600); pg.wait_for_timeout(500)
    check("Vuốt xuống -> tháng trước", tieude(pg) == m0)
    vuot(cdp, 300, 400, 80, 400); pg.wait_for_timeout(500)
    check("Tháng: vuốt ngang trái -> tháng sau", tieude(pg) == m1)
    check("Không bật hộp thoại ngoài ý muốn", not pg.evaluate("document.getElementById('ov').classList.contains('on')"))

    print("5) Chạm vẫn mở hộp thoại")
    pg.tap(".o >> nth=10"); pg.wait_for_timeout(300)
    check("Chạm ô ngày mở hộp tạo sự kiện", pg.evaluate("document.getElementById('ov').classList.contains('on')"))
    check("Không có lỗi JS", not errs)
    b.close()
print("TẤT CẢ ĐẠT" if ok_all else "CÓ MỤC HỎNG"); sys.exit(0 if ok_all else 1)
