"""Thử 2.7 (Trợ lý gõ câu tự nhiên) bằng Gemini GIẢ + Supabase GIẢ. Không gọi mạng thật, không đụng dữ liệu thật.
Chạy CHÍNH mã trong supabase/functions/tro-ly/index.ts (bóc kiểu TypeScript bằng regex) bên trong Chrome (máy không có Deno),
nối thẳng với giao diện index.html: gõ câu -> function -> xem trước -> Đồng ý/Huỷ -> bảng giả.
Chạy: py -3.12 tools/thu_tro_ly_gia.py [thu_muc_ra]   (mặc định docs/bang-chung/2.7; KHÔNG dùng -I)"""
import os, sys, re, json, datetime as dt
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'bang-chung', '2.7')
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, 'thu-tro-ly.txt'), 'w', encoding='utf-8')
def say(*a):
    t = ' '.join(str(x) for x in a); print(t); LOG.write(t + '\n'); LOG.flush()

# ---- bóc TypeScript -> JavaScript ----
code = open(os.path.join(ROOT, 'supabase/functions/tro-ly/index.ts'), encoding='utf-8').read()
code = re.sub(r"^import .*$", "", code, flags=re.M)
code = re.sub(r"\b(\w+): any\b", r"\1", code)
code = re.sub(r"\)!", ")", code)

# ---- ngày mong đợi (giờ Việt Nam) ----
vn = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
hom_nay = vn.date()
mai = hom_nay + dt.timedelta(days=1)
t6 = hom_nay + dt.timedelta(days=((4 - hom_nay.weekday()) % 7) or 7)  # thứ 6 sắp tới
iso = lambda d: d.strftime('%Y-%m-%d')

GEM = {
    'chiều thứ 6 họp khách 3h': dict(loai='su_kien', tieu_de='Họp khách', ngay=iso(t6), gio_bat_dau='15:00', thoi_luong_phut=60, loai_viec='cv', ca_ngay=False),
    'ý tưởng: làm kênh review đồ bếp': dict(loai='y_tuong', tieu_de='Làm kênh review đồ bếp', ghi_chu=None, uu_tien='cao', nhan=['video', '#bếp']),
    'mai 7h sáng quay video son': dict(loai='su_kien', tieu_de='Quay video son', ngay=iso(mai), gio_bat_dau='07:00', gio_ket_thuc=None, thoi_luong_phut=90, loai_viec='vd'),
    'asdf qwer zxcv': dict(loai='khong_hieu'),
    'ngày rác': dict(loai='su_kien', tieu_de='Việc lạ', ngay='2026-13-45', gio_bat_dau='25:99', gio_ket_thuc='xx', nhac_phut=-5, loai_viec='khong-co-that'),
    'cả ngày mai đi chợ': dict(loai='su_kien', tieu_de='Đi chợ', ngay=iso(mai), ca_ngay=True),
    'gio nguoc': dict(loai='su_kien', tieu_de='Giờ ngược', ngay=iso(hom_nay), gio_bat_dau='10:00', gio_ket_thuc='09:00'),
    'khuya': dict(loai='su_kien', tieu_de='Họp khuya', ngay=iso(hom_nay), gio_bat_dau='23:30', thoi_luong_phut=120, nhac_phut=30),
}
CATS = [dict(id='cv', ten='Công việc', mau='#1a73e8', thu_tu=1), dict(id='vd', ten='Video', mau='#e8710a', thu_tu=2), dict(id='cn', ten='Cá nhân', mau='#0b8043', thu_tu=3)]

FAKE = """
window.__DB={su_kien:[],y_tuong:[]}; window.__RT={}; let __n=100;
const DEF={y_tuong:()=>({ghi_chu:null,trang_thai:'chua_lam',uu_tien:'vua',nhan:[],han:null,thu_tu:0,tao_luc:new Date().toISOString(),sua_luc:new Date().toISOString(),xoa_luc:null,nguon:null,link:null}),
 su_kien:()=>({xoa_luc:null,lap:'none',lap_den:null,lap_ngoai:[],ghi_chu:null})};
window.supabase={createClient:()=>{
 const q=(t)=>{const o={f:[],op:'select',pl:null,ord:null,
  select:()=>o,order:(c)=>{o.ord=c;return o},
  is:(c,v)=>{o.f.push(r=>r[c]==v);return o}, not:(c,_,v)=>{o.f.push(r=>r[c]!=v);return o},
  eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, lt:(c,v)=>{o.f.push(r=>r[c]!=null&&r[c]<v);return o},
  insert:(p)=>{o.op='insert';o.pl=p;return o}, update:(p)=>{o.op='update';o.pl=p;return o}, delete:()=>{o.op='delete';return o},
  then:(res)=>{ if(t=='app_owner') return res({data:[{user_id:'u1'}],error:null});
   if(t=='loai_viec') return res({data:__CATS__,error:null});
   const D=window.__DB[t]; const m=D.filter(r=>o.f.every(f=>f(r)));
   if(o.op=='insert'){ if(window.__luuLoi) return res({data:null,error:{message:'giả: lỗi lưu'}});
     const rows=[].concat(o.pl).map(p=>({id:'n'+(++__n),...DEF[t](),...p}));rows.forEach(r=>D.push(r));return res({data:null,error:null});}
   if(o.op=='update'){m.forEach(r=>Object.assign(r,o.pl));return res({data:null,error:null});}
   if(o.op=='delete'){window.__DB[t]=D.filter(r=>!m.includes(r));return res({data:null,error:null});}
   const out=JSON.parse(JSON.stringify(m)); if(o.ord) out.sort((a,b)=>(a[o.ord]>b[o.ord])-(a[o.ord]<b[o.ord]));
   return res({data:out,error:null}); }};return o};
 const ch={on:(_,f,cb)=>{window.__RT[f.table]=cb;return ch},subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'thu@gia'},access_token:'TOKEN-GIA'}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};

// ---- Edge Function tro-ly thật (mã index.ts) + Gemini giả ----
window.__GEM = __GEM__; window.__gemMode = 'ok'; window.__gemCalls = 0; window.__gemLast = null; window.__laChu = true;
window.__fnEnv = { GEMINI_API_KEY: 'KHOA-GIA-CHI-DE-TEST', SUPABASE_URL: 'https://gia', SUPABASE_ANON_KEY: 'anon-gia' };
(function(){
  const Deno = { env: { get: (k) => window.__fnEnv[k] }, serve: (h) => { window.__H = h; } };
  const createClient = () => ({ rpc: async () => ({ data: window.__laChu, error: null }) });
  const fakeFetch = async (url, init) => {
    window.__gemCalls++; const body = JSON.parse(init.body);
    window.__gemLast = { url, key: init.headers['x-goog-api-key'], sys: body.systemInstruction.parts[0].text, cau: body.contents[0].parts[0].text, cfg: body.generationConfig };
    const m = window.__gemMode;
    if (m === 'net') throw new Error('mạng chết');
    if (m === '429') return new Response('{}', { status: 429 });
    if (m === '500') return new Response('{}', { status: 500 });
    if (m === '403') return new Response('{}', { status: 403 });
    const wrap = (t) => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: t }] } }] }), { status: 200 });
    if (m === 'junk') return wrap('không phải json {{');
    if (m === 'empty') return new Response(JSON.stringify({ candidates: [] }), { status: 200 });
    return wrap(JSON.stringify(window.__GEM[window.__gemLast.cau] || { loai: 'khong_hieu' }));
  };
  new Function('Deno', 'createClient', 'fetch', __CODE__)(Deno, createClient, fakeFetch);
  const real = window.fetch.bind(window);
  window.fetch = async (u, i) => {
    if (String(u).includes('/functions/v1/tro-ly')) {
      const hd = new Headers((i && i.headers) || {});
      return window.__H({ method: (i && i.method) || 'POST', headers: hd, json: async () => JSON.parse(i.body) });
    }
    return real(u, i);
  };
})();
""".replace('__CATS__', json.dumps(CATS)).replace('__GEM__', json.dumps(GEM)).replace('__CODE__', json.dumps(code))

ok_all = True
def check(ten, cond, extra=''):
    global ok_all
    ok_all &= bool(cond); say(('  ĐẠT  ' if cond else '  HỎNG ') + ten + ((' ' + str(extra)) if (extra and not cond) else ''))
def tbl(pg, t): return pg.evaluate("t=>window.__DB[t]", t)
def shot(pg, name): pg.screenshot(path=os.path.join(OUT, name))
def mo(browser, **kw):
    ctx = browser.new_context(**kw); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    pg.on("dialog", lambda d: d.accept())
    pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=FAKE, content_type="application/javascript"))
    pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
    pg.wait_for_selector("#app:not([hidden])")
    return ctx, pg, errs
def hoi(pg, cau, mode='ok'):
    """Gõ câu vào Trợ lý, đợi tới khi có khung xem trước hoặc dòng lỗi."""
    pg.evaluate("m=>window.__gemMode=m", mode)
    if not pg.locator("#ov.on #tlCau").count(): pg.click("#fabTl"); pg.wait_for_selector("#ov.on #tlCau")
    pg.fill("#tlCau", cau); pg.click("#tlGui")
    pg.wait_for_selector("#ov.on #tlOk, #ov.on #tlLoi:not([hidden])", timeout=8000)
def loi_txt(pg): return pg.inner_text("#tlLoi") if pg.locator("#tlLoi:not([hidden])").count() else ''
def dong(pg):
    if pg.locator("#ov.on").count(): pg.evaluate("dongHop()")
def call(pg, cau, **kw):
    """Gọi thẳng function (không qua giao diện) để thử các trường hợp biên."""
    return pg.evaluate("""async ([cau, kw]) => {
      const hd = kw.auth === false ? {} : { Authorization: 'Bearer TOKEN-GIA' };
      const r = await fetch('https://gia/functions/v1/tro-ly', { method: 'POST', headers: hd, body: JSON.stringify({ cau, loai_viec: kw.lv || [] }) });
      const t = await r.text(); let j = null; try { j = JSON.parse(t); } catch (e) {}
      return { status: r.status, j, t };
    }""", [cau, kw])

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx, pg, errs = mo(b, viewport=dict(width=1200, height=800))
    check("Có nút ✨ Trợ lý trên máy tính", pg.locator("#fabTl").is_visible())

    say("1) 'chiều thứ 6 họp khách 3h' -> sự kiện đúng")
    pg.click("#fabTl"); pg.wait_for_selector("#tlCau"); shot(pg, "01-truoc-hop-nhap.png")
    hoi(pg, "chiều thứ 6 họp khách 3h")
    check("Hiện khung xem trước SỰ KIỆN", pg.locator("#tlXem:has-text('Sự kiện mới')").count() == 1)
    check("Tiêu đề 'Họp khách', ngày %s (thứ 6 sắp tới)" % iso(t6), pg.input_value("#pTen") == "Họp khách" and pg.input_value("#pNgay") == iso(t6))
    check("Giờ 15:00 – 16:00 (3h chiều, mặc định 60 phút), loại Công việc, nhắc 15 phút",
          pg.input_value("#pG1") == "15:00" and pg.input_value("#pG2") == "16:00" and pg.input_value("#pLoai") == "cv" and pg.input_value("#pNhac") == "15")
    check("CHƯA lưu gì trước khi bấm Đồng ý", len(tbl(pg, 'su_kien')) == 0)
    sysm = pg.evaluate("window.__gemLast.sys")
    check("Gemini được cho biết ngày hiện tại %s + thứ trong tuần + múi giờ VN" % iso(hom_nay), iso(hom_nay) in sysm and 'Thứ sáu' in sysm and 'Việt Nam' in sysm)
    check("Chỉ 1 lần gọi Gemini cho câu này, model nhẹ, ép JSON", pg.evaluate("window.__gemCalls") == 1 and 'flash-lite' in pg.evaluate("window.__gemLast.url") and pg.evaluate("window.__gemLast.cfg.responseMimeType") == 'application/json')
    check("Khoá Gemini chỉ nằm trong header gọi Gemini, KHÔNG có trong trang/kết quả", 'KHOA-GIA' not in pg.content() and pg.evaluate("window.__gemLast.key") == 'KHOA-GIA-CHI-DE-TEST')
    shot(pg, "02-xem-truoc-su-kien.png")
    pg.click("#tlOk"); pg.wait_for_timeout(500)
    sk = tbl(pg, 'su_kien')
    when = pg.evaluate("r=>{const d=new Date(r.bat_dau),e=new Date(r.ket_thuc),p=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes())+'-'+p(e.getHours())+':'+p(e.getMinutes())}", sk[0]) if sk else ''
    check("Đồng ý -> lưu 1 sự kiện đúng cột: tiêu đề, giờ, loại, nhắc, không lặp", len(sk) == 1 and sk[0]['tieu_de'] == 'Họp khách' and when == iso(t6) + ' 15:00-16:00' and sk[0]['loai'] == 'cv' and sk[0]['nhac_phut'] == 15 and sk[0]['lap'] == 'none' and sk[0]['ca_ngay'] is False, when)
    check("Hộp thoại đóng, lịch hiện sự kiện mới", pg.locator("#ov.on").count() == 0 and pg.locator(".ev:has-text('Họp khách')").count() >= 1)
    shot(pg, "03-sau-khi-dong-y.png")

    say("2) 'ý tưởng: làm kênh review đồ bếp' -> vào Kho ý tưởng")
    hoi(pg, "ý tưởng: làm kênh review đồ bếp")
    check("Hiện khung xem trước Ý TƯỞNG (ưu tiên Cao, nhãn video, bếp — bỏ dấu #)", pg.locator("#tlXem:has-text('Ý tưởng mới')").count() == 1 and pg.input_value("#pUu") == "cao" and pg.input_value("#pNhan") == "video, bếp")
    shot(pg, "04-xem-truoc-y-tuong.png")
    pg.click("#tlOk"); pg.wait_for_timeout(500)
    yt = tbl(pg, 'y_tuong')
    check("Đồng ý -> lưu ý tưởng: Chưa làm, ưu tiên cao, nhãn [video, bếp]", len(yt) == 1 and yt[0]['tieu_de'] == 'Làm kênh review đồ bếp' and yt[0]['trang_thai'] == 'chua_lam' and yt[0]['uu_tien'] == 'cao' and yt[0]['nhan'] == ['video', 'bếp'])
    check("Chuyển sang trang Kho ý tưởng và thấy thẻ mới", pg.locator("#p-y.on .card:has-text('review đồ bếp')").count() == 1)
    shot(pg, "05-kho-y-tuong-sau-khi-them.png")

    say("3) Câu vô nghĩa -> không tạo gì")
    n0, m0 = len(tbl(pg, 'su_kien')), len(tbl(pg, 'y_tuong'))
    hoi(pg, "asdf qwer zxcv")
    check("Báo 'chưa hiểu' bằng tiếng Việt, không có khung xem trước", 'chưa hiểu' in loi_txt(pg) and pg.locator("#tlOk").count() == 0, loi_txt(pg))
    check("Không lưu gì", len(tbl(pg, 'su_kien')) == n0 and len(tbl(pg, 'y_tuong')) == m0)
    shot(pg, "06-cau-vo-nghia.png"); dong(pg)

    say("4) Gemini lỗi / hết lượt -> báo thân thiện, không sập")
    hoi(pg, "chiều thứ 6 họp khách 3h", '429')
    check("Hết lượt (429): thông báo tiếng Việt", 'hết lượt' in loi_txt(pg) and pg.locator("#tlOk").count() == 0, loi_txt(pg))
    shot(pg, "07-gemini-het-luot.png")
    hoi(pg, "chiều thứ 6 họp khách 3h", '500')
    check("Gemini 500: 'đang bận, thử lại'", 'bận' in loi_txt(pg), loi_txt(pg))
    hoi(pg, "chiều thứ 6 họp khách 3h", 'net')
    check("Mất mạng tới Gemini: báo thân thiện", 'kết nối' in loi_txt(pg), loi_txt(pg))
    hoi(pg, "chiều thứ 6 họp khách 3h", 'junk')
    check("Gemini trả rác không phải JSON: báo thân thiện", 'chưa đúng dạng' in loi_txt(pg), loi_txt(pg))
    hoi(pg, "chiều thứ 6 họp khách 3h", 'empty')
    check("Gemini không có đáp án: báo thân thiện", 'không trả lời được' in loi_txt(pg), loi_txt(pg))
    hoi(pg, "chiều thứ 6 họp khách 3h", '403')
    check("Khoá Gemini sai: nhắc kiểm tra GEMINI_API_KEY (không in khoá)", 'GEMINI_API_KEY' in loi_txt(pg) and 'KHOA-GIA' not in loi_txt(pg), loi_txt(pg))
    check("Sau mọi lỗi vẫn không lưu gì thêm", len(tbl(pg, 'su_kien')) == n0 and len(tbl(pg, 'y_tuong')) == m0)
    hoi(pg, "chiều thứ 6 họp khách 3h", 'ok')
    check("Hết lỗi thì dùng lại được ngay (hiện xem trước)", pg.locator("#tlOk").count() == 1)
    dong(pg)

    say("5) Sửa trong khung xem trước rồi Đồng ý")
    hoi(pg, "mai 7h sáng quay video son")
    check("AI hiểu: mai (%s) 07:00–08:30 (90 phút), loại Video" % iso(mai), pg.input_value("#pNgay") == iso(mai) and pg.input_value("#pG1") == "07:00" and pg.input_value("#pG2") == "08:30" and pg.input_value("#pLoai") == "vd")
    pg.fill("#pTen", "Quay video son môi"); pg.fill("#pNgay", iso(mai + dt.timedelta(days=1)))
    pg.fill("#pG1", "08:30"); pg.fill("#pG2", "10:00"); pg.select_option("#pLoai", "cn"); pg.select_option("#pNhac", "60"); pg.fill("#pGhi", "Mang đèn")
    shot(pg, "08-dang-sua-trong-xem-truoc.png")
    pg.click("#tlOk"); pg.wait_for_timeout(500)
    r = [x for x in tbl(pg, 'su_kien') if 'son' in x['tieu_de']]
    when = pg.evaluate("r=>{const d=new Date(r.bat_dau),e=new Date(r.ket_thuc),p=n=>String(n).padStart(2,'0');return d.getFullYear()+'-'+p(d.getMonth()+1)+'-'+p(d.getDate())+' '+p(d.getHours())+':'+p(d.getMinutes())+'-'+p(e.getHours())+':'+p(e.getMinutes())}", r[0]) if r else ''
    check("Lưu đúng bản ĐÃ SỬA (tên, ngày+1, 08:30–10:00, Cá nhân, nhắc 60, ghi chú)", len(r) == 1 and r[0]['tieu_de'] == 'Quay video son môi' and when == iso(mai + dt.timedelta(days=1)) + ' 08:30-10:00' and r[0]['loai'] == 'cn' and r[0]['nhac_phut'] == 60 and r[0]['ghi_chu'] == 'Mang đèn', when)

    say("6) Huỷ -> không lưu gì")
    n1 = len(tbl(pg, 'su_kien'))
    hoi(pg, "chiều thứ 6 họp khách 3h")
    pg.click("#tlHuy"); pg.wait_for_timeout(300)
    check("Bấm Huỷ: đóng hộp thoại, số sự kiện không đổi", pg.locator("#ov.on").count() == 0 and len(tbl(pg, 'su_kien')) == n1)
    hoi(pg, "ý tưởng: làm kênh review đồ bếp"); m1 = len(tbl(pg, 'y_tuong'))
    pg.click("#ov", position=dict(x=5, y=5)); pg.wait_for_timeout(300)
    check("Bấm ra ngoài khung: đóng, không lưu ý tưởng", pg.locator("#ov.on").count() == 0 and len(tbl(pg, 'y_tuong')) == m1)
    hoi(pg, "chiều thứ 6 họp khách 3h"); pg.fill("#pTen", "   "); pg.click("#tlOk"); pg.wait_for_timeout(200)
    check("Xoá trống tiêu đề rồi Đồng ý: không lưu, báo nhập tiêu đề", len(tbl(pg, 'su_kien')) == n1 and pg.locator("#toast:has-text('tiêu đề')").count() == 1)
    pg.evaluate("window.__luuLoi=true"); pg.fill("#pTen", "Thử lỗi lưu"); pg.click("#tlOk"); pg.wait_for_timeout(300)
    check("Lưu vào Supabase lỗi: báo lỗi, giữ khung để thử lại, không mất dữ liệu gõ", pg.locator("#toast:has-text('Lưu lỗi')").count() == 1 and pg.locator("#tlOk:not([disabled])").count() == 1 and pg.input_value("#pTen") == "Thử lỗi lưu")
    pg.evaluate("window.__luuLoi=false"); dong(pg)

    say("7) Kiểm tra bảo vệ + giới hạn (gọi thẳng function)")
    g0 = pg.evaluate("window.__gemCalls"); pg.evaluate("window.__gemMode='ok'")
    r = call(pg, "x" * 501)
    check("Câu > 500 ký tự: bị từ chối 400, KHÔNG gọi Gemini", r['status'] == 400 and 'dài quá' in r['j']['loi'] and pg.evaluate("window.__gemCalls") == g0)
    r = call(pg, "x" * 500, ); check("Câu đúng 500 ký tự: được nhận (gọi Gemini)", r['status'] == 200 and pg.evaluate("window.__gemCalls") == g0 + 1)
    g0 = pg.evaluate("window.__gemCalls")
    r = call(pg, "   "); check("Câu rỗng: 400, không gọi Gemini", r['status'] == 400 and pg.evaluate("window.__gemCalls") == g0)
    r = call(pg, "họp", auth=False); check("Không có token đăng nhập: 401, không gọi Gemini", r['status'] == 401 and pg.evaluate("window.__gemCalls") == g0)
    pg.evaluate("window.__laChu=false"); r = call(pg, "chiều thứ 6 họp khách 3h")
    check("Người không phải chủ app: 403, không gọi Gemini", r['status'] == 403 and pg.evaluate("window.__gemCalls") == g0)
    pg.evaluate("window.__laChu=true; window.__fnEnv.GEMINI_API_KEY=undefined"); r = call(pg, "chiều thứ 6 họp khách 3h")
    check("Chưa cài GEMINI_API_KEY: báo hướng dẫn (500), không sập", r["status"] == 500 and "chưa được cài" in r["j"]["loi"] and "KHOA-GIA" not in r["t"])
    pg.evaluate("window.__fnEnv.GEMINI_API_KEY='KHOA-GIA-CHI-DE-TEST'")

    say("8) Làm sạch đầu ra của Gemini (không tin AI)")
    r = call(pg, "ngày rác")['j']
    check("Ngày/giờ/nhắc vô lý -> về ngày hôm nay, cả ngày, không nhắc, loại việc lạ bị bỏ", r['ngay'] == iso(hom_nay) and r['ca_ngay'] is True and r['gio_bat_dau'] is None and r['nhac_phut'] is None and r['loai_viec'] is None, r)
    r = call(pg, "cả ngày mai đi chợ")['j']; check("Sự kiện cả ngày: không giờ, không nhắc mặc định", r['ca_ngay'] is True and r['gio_bat_dau'] is None and r['nhac_phut'] is None)
    r = call(pg, "gio nguoc")['j']; check("Giờ kết thúc <= bắt đầu -> tự sửa thành +60 phút (10:00–11:00)", r['gio_bat_dau'] == '10:00' and r['gio_ket_thuc'] == '11:00', r)
    r = call(pg, "khuya")['j']; check("Họp kéo qua nửa đêm -> chặn ở 23:59, giữ nhắc 30 phút", r['gio_ket_thuc'] == '23:59' and r['nhac_phut'] == 30, r)
    r = call(pg, "chiều thứ 6 họp khách 3h", lv=[dict(id='cv', ten='Công việc')])['j']; check("Loại việc hợp lệ trong danh sách được giữ", r['loai_viec'] == 'cv')
    r = call(pg, "chiều thứ 6 họp khách 3h", lv=[dict(id='khac', ten='Khác')])['j']; check("Loại việc không có trong danh sách bị bỏ", r['loai_viec'] is None)
    check("Gemini được nhắc: nội dung câu chỉ là dữ liệu (chống chèn lệnh)", 'DỮ LIỆU' in pg.evaluate("window.__gemLast.sys"))
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS: %s' % errs, not errs)
    ctx.close()

    say("9) Điện thoại (390x800, cảm ứng)")
    ctx, pg, errs = mo(b, viewport=dict(width=390, height=800), has_touch=True, is_mobile=True, device_scale_factor=2)
    check("Nút ✨ nằm trên nút + và không đè lên nhau", pg.locator("#fabTl").is_visible() and pg.locator("#fab").is_visible() and pg.locator("#fabTl").bounding_box()['y'] + 52 <= pg.locator("#fab").bounding_box()['y'] + 1)
    pg.tap("#fabTl"); pg.wait_for_selector("#tlCau"); shot(pg, "09-dien-thoai-nhap.png")
    pg.fill("#tlCau", "chiều thứ 6 họp khách 3h"); pg.tap("#tlGui"); pg.wait_for_selector("#tlOk")
    bb = pg.locator("#dlg").bounding_box()
    check("Khung xem trước vừa màn hình điện thoại (không tràn ngang)", bb['x'] >= 0 and bb['x'] + bb['width'] <= 390 and pg.evaluate("document.documentElement.scrollWidth") <= 390)
    shot(pg, "10-dien-thoai-xem-truoc.png")
    pg.tap("#tlOk"); pg.wait_for_timeout(500)
    check("Đồng ý trên điện thoại lưu được", len([x for x in tbl(pg, 'su_kien') if x['tieu_de'] == 'Họp khách']) == 1)
    pg.tap("#fabTl"); pg.wait_for_selector("#tlCau"); pg.tap(".tl-goi button:nth-child(2)"); pg.wait_for_selector("#tlOk")
    check("Bấm câu gợi ý (chip) hoạt động", pg.locator("#tlXem:has-text('Ý tưởng mới')").count() == 1)
    pg.tap("#tlHuy"); pg.wait_for_timeout(200)
    check("Huỷ trên điện thoại: không lưu ý tưởng", len(tbl(pg, 'y_tuong')) == 0)
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS (điện thoại): %s' % errs, not errs)
    ctx.close(); b.close()
say("TẤT CẢ ĐẠT" if ok_all else "CÓ LỖI")
sys.exit(0 if ok_all else 1)
