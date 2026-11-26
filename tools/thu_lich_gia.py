"""Thử giao diện Lịch bằng dữ liệu GIẢ (không đụng Supabase thật). Chạy: py -3.12 tools/thu_lich_gia.py <thu_muc_anh>"""
import os, sys, json, datetime as dt
from playwright.sync_api import sync_playwright
OUT = sys.argv[1]; os.makedirs(OUT, exist_ok=True)
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
now = dt.datetime.now().astimezone()
def at(h, m=0, d=0): return (now.replace(hour=h, minute=m, second=0, microsecond=0) + dt.timedelta(days=d)).isoformat()
EVS = [
 dict(id='1', tieu_de='Họp khách', ghi_chu=None, bat_dau=at(15), ket_thuc=at(16), ca_ngay=False, loai='cv', xoa_luc=None),
 dict(id='2', tieu_de='Quay video son', ghi_chu=None, bat_dau=at(15,30), ket_thuc=at(17), ca_ngay=False, loai='vd', xoa_luc=None),
 dict(id='3', tieu_de='Đi khám', ghi_chu=None, bat_dau=at(9,0,1), ket_thuc=at(10,0,1), ca_ngay=False, loai='cn', xoa_luc=None),
 dict(id='4', tieu_de='Sinh nhật mẹ', ghi_chu=None, bat_dau=at(0,0,2), ket_thuc=at(0,0,3), ca_ngay=True, loai='gd', xoa_luc=None),
]
CATS = [dict(id='cv',ten='Công việc',mau='#1a73e8',thu_tu=1),dict(id='vd',ten='Quay/làm video',mau='#d50000',thu_tu=2),dict(id='cn',ten='Cá nhân/sức khoẻ',mau='#0b8043',thu_tu=3),dict(id='gd',ten='Gia đình',mau='#f4511e',thu_tu=4),dict(id='ht',ten='Học tập',mau='#8e24aa',thu_tu=5)]
FAKE = """
window.supabase={createClient:()=>{
 const q=(t)=>{const o={select:()=>o,order:()=>o,is:()=>o,eq:()=>o,insert:()=>o,update:()=>o,delete:()=>o,lt:()=>o,not:()=>o,then:(f)=>f({data:t=='app_owner'?[{user_id:'u1'}]:(t=='su_kien'?%s:%s),error:null})};return o};
 const ch={on:()=>ch,subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'thu@gia'}}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};
""" % (json.dumps(EVS), json.dumps(CATS))
with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    for ten, vp, mobile in [("may-tinh", dict(width=1200,height=800), False), ("dien-thoai", dict(width=390,height=780), True)]:
        ctx = b.new_context(viewport=vp, is_mobile=mobile, device_scale_factor=1)
        pg = ctx.new_page()
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))
        pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=FAKE, content_type="application/javascript"))
        pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
        pg.wait_for_selector("#app:not([hidden])")
        pg.wait_for_timeout(500)
        pg.screenshot(path=os.path.join(OUT, f"{ten}-tuan-ngay.png"))
        print(ten, "so su kien tren luoi:", pg.locator(".ev, .ev-ngay").count(), "| loi JS:", errs)
        pg.select_option("#chonKieu", "month"); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(OUT, f"{ten}-thang.png"))
        pg.select_option("#chonKieu", "week"); pg.click(".ev >> nth=0"); pg.wait_for_timeout(200)
        pg.screenshot(path=os.path.join(OUT, f"{ten}-hop-thoai.png"))
        ctx.close()
    b.close()
