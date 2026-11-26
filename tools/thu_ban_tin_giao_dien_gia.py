"""Thử giao diện trang "Bản tin" (2.9) bằng Supabase GIẢ + function ban-tin-gui GIẢ trong bộ nhớ. Không gọi mạng thật.
Chạy: py -3.12 tools/thu_ban_tin_giao_dien_gia.py [thu_muc_ra]   (mặc định docs/bang-chung/2.9; KHÔNG dùng -I)"""
import os, sys, json, datetime as dt
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'bang-chung', '2.9')
os.makedirs(OUT, exist_ok=True)
LOG = open(os.path.join(OUT, 'thu-giao-dien-ban-tin.txt'), 'w', encoding='utf-8')
def say(*a):
    t = ' '.join(str(x) for x in a); print(t); LOG.write(t + '\n'); LOG.flush()

vn = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None) + dt.timedelta(hours=7)
def ngay(n): return (vn.date() - dt.timedelta(days=n)).strftime('%Y-%m-%d')
now = dt.datetime.now().astimezone()
def ago(days): return (now - dt.timedelta(days=days)).isoformat()

def tin(cd, bao, td, ts, link, ngon='vi', ai=True, trung=None):
    d = dict(chu_de=cd, bao=bao, tieu_de=td, tom_tat=ts, link=link, ngon_ngu=ngon, ai=ai)
    if trung: d['trung_voi'] = trung
    return d
TIN_HOM_NAY = [
    tin('Thời sự trong nước', 'VnExpress', 'Quốc hội thông qua luật đất đai sửa đổi', 'Luật có hiệu lực từ năm tới. Các địa phương công bố bảng giá đất mới.', 'https://vnexpress.net/a-1', trung=['Tuổi Trẻ']),
    tin('Thời sự trong nước', 'Thanh Niên', '<img src=x onerror="window.__xss=1"> Tin có thẻ HTML', 'Tóm tắt có <script>window.__xss=2</script> và "ngoặc" & ký tự', 'https://thanhnien.vn/b?x=1&y=2'),
    tin('Thế giới', 'BBC', 'Hội nghị khí hậu kết thúc với thoả thuận về quỹ hỗ trợ', 'Các nước đồng ý tăng đóng góp cho quỹ thích ứng.', 'https://bbc.co.uk/c'),
    tin('Kinh tế – tài chính', 'Thanh Niên', 'Giá vàng trong nước giảm nhẹ', 'Vàng miếng giảm khoảng 300.000 đồng/lượng.', 'javascript:window.__xss=3'),
    tin('Công nghệ – AI', 'VOV', 'Việt Nam thí điểm chứng thư số trên VNeID', 'Người dân có thể ký số ngay trên điện thoại.', 'https://vov.vn/d'),
    tin('Kinh doanh online / TMĐT', 'Tuổi Trẻ', 'Sàn TMĐT siết quy định hàng giả', 'Người bán phải bổ sung giấy tờ nguồn gốc.', 'https://tuoitre.vn/e'),
    tin('Sức khoẻ', 'Báo Chính phủ', 'Bộ Y tế khuyến cáo phòng cúm mùa', 'Người cao tuổi nên tiêm phòng.', 'https://baochinhphu.vn/f'),
    tin('Thể thao', 'The Guardian', 'Premier League leaders win 2-0', 'The result extends the lead to four points.', 'https://theguardian.com/g', ngon='en', ai=False),
]
def nd(ngay_, tins, dung_ai=True, dau=None, loi_nguon=None):
    return dict(phien_ban=1, ngay=ngay_, tao_luc=ago(0), dung_ai=dung_ai, ly_do_khong_ai=None if dung_ai else 'Gemini hết lượt miễn phí (429)', so_lan_gemini=1,
                loi_nguon=loi_nguon or [], tin=tins,
                dau=dau or dict(lich=[dict(gio=None, gio_ket=None, ca_ngay=True, tieu_de='Sinh nhật mẹ'), dict(gio='09:00', gio_ket='10:00', ca_ngay=False, tieu_de='Họp khách <b>quan trọng</b>')],
                                tre_han=[dict(tieu_de='Nộp báo cáo thuế', han=ngay(3))], de_lau=[dict(tieu_de='Làm kênh review đồ bếp', so_ngay=20)]))
BT = [dict(ngay=ngay(0), noi_dung=nd(ngay(0), TIN_HOM_NAY, loi_nguon=['NHK World (Thế giới)']), tao_luc=ago(0), telegram_luc=now.replace(hour=8, minute=0, second=3).isoformat(), loi=None),
      dict(ngay=ngay(1), noi_dung=nd(ngay(1), [tin('Thế giới', 'DW', 'Germany unveils rail investment plan', 'Germany will spend more on its aging rail network.', 'https://dw.com/h', ngon='en', ai=False),
                                               tin('Thể thao', 'VnExpress', 'Tuyển Việt Nam chốt danh sách dự giải', 'HLV triệu tập 26 cầu thủ.', 'https://vnexpress.net/i')], dung_ai=False,
                                     dau=dict(lich=[], tre_han=[], de_lau=[])), tao_luc=ago(1), telegram_luc=None, loi='Gemini: Gemini hết lượt miễn phí (429)'),
      dict(ngay=ngay(2), noi_dung=nd(ngay(2), [tin('Sức khoẻ', 'BBC', 'Ngủ đủ giấc giúp giảm nguy cơ tim mạch', 'Nghiên cứu theo dõi 90.000 người.', 'https://bbc.co.uk/j')]), tao_luc=ago(2), telegram_luc=ago(2), loi=None)]
YT = [dict(id='y1', tieu_de='Làm kênh review đồ bếp', ghi_chu=None, trang_thai='chua_lam', uu_tien='cao', nhan=['video'], han=None, thu_tu=1, tao_luc=ago(20), sua_luc=ago(20), xoa_luc=None, nguon=None, link=None)]
CATS = [dict(id='cv', ten='Công việc', mau='#1a73e8', thu_tu=1)]

FAKE = """
(function(){ let saved=null; try{saved=JSON.parse(localStorage.getItem('__fdb')||'null')}catch(_){}
 window.__DB=saved||{su_kien:[],y_tuong:%s,ban_tin:%s}; })();
window.__RT={}; let __n=100; window.__goi=[]; window.__fnMode='ok';
const __luuDb=()=>localStorage.setItem('__fdb',JSON.stringify(window.__DB));
const DEF={y_tuong:()=>({ghi_chu:null,trang_thai:'chua_lam',uu_tien:'vua',nhan:[],han:null,thu_tu:0,tao_luc:new Date().toISOString(),sua_luc:new Date().toISOString(),xoa_luc:null,nguon:null,link:null}),
 su_kien:()=>({xoa_luc:null,lap:'none',lap_den:null,lap_ngoai:[],ghi_chu:null})};
window.supabase={createClient:()=>{
 const q=(t)=>{const o={f:[],op:'select',pl:null,ord:null,desc:false,lim:null,
  select:()=>o,order:(c,op)=>{o.ord=c;o.desc=!!(op&&op.ascending===false);return o},limit:(n)=>{o.lim=n;return o},
  is:(c,v)=>{o.f.push(r=>r[c]==v);return o}, not:(c,_,v)=>{o.f.push(r=>r[c]!=v);return o},
  eq:(c,v)=>{o.f.push(r=>r[c]===v);return o}, lt:(c,v)=>{o.f.push(r=>r[c]!=null&&r[c]<v);return o},
  insert:(p)=>{o.op='insert';o.pl=p;return o}, update:(p)=>{o.op='update';o.pl=p;return o}, delete:()=>{o.op='delete';return o},
  then:(res)=>{ if(t=='app_owner') return res({data:[{user_id:'u1'}],error:null});
   if(t=='loai_viec') return res({data:%s,error:null});
   if(t=='ban_tin'&&localStorage.getItem('__btloi')) return res({data:null,error:{message:'giả: mất mạng'}});
   const D=window.__DB[t]; const m=D.filter(r=>o.f.every(f=>f(r)));
   if(o.op=='insert'){if(window.__luuLoi) return res({data:null,error:{message:'giả: lỗi lưu'}});
     const rows=[].concat(o.pl).map(p=>({id:'n'+(++__n),...DEF[t](),...p}));rows.forEach(r=>D.push(r));__luuDb();return res({data:null,error:null});}
   if(o.op=='update'){m.forEach(r=>Object.assign(r,o.pl));__luuDb();return res({data:null,error:null});}
   if(o.op=='delete'){window.__DB[t]=D.filter(r=>!m.includes(r));__luuDb();return res({data:null,error:null});}
   let out=JSON.parse(JSON.stringify(m)); if(o.ord){out.sort((a,b)=>(a[o.ord]>b[o.ord])-(a[o.ord]<b[o.ord]));if(o.desc)out.reverse();}
   if(o.lim)out=out.slice(0,o.lim);
   return res({data:out,error:null}); }};return o};
 const ch={on:(_,f,cb)=>{window.__RT[f.table]=cb;return ch},subscribe:()=>ch};
 return {from:q,channel:()=>ch,auth:{getSession:async()=>({data:{session:{user:{id:'u1',email:'thu@gia'},access_token:'TOKEN-GIA'}}}),onAuthStateChange:()=>{},signOut:async()=>{},signInWithOAuth:()=>{}}}}};
// function ban-tin-gui giả
const __real=window.fetch.bind(window);
window.fetch=async(u,i)=>{
 if(String(u).includes('/functions/v1/ban-tin-gui')){
  const body=JSON.parse(i.body); window.__goi.push({auth:(i.headers||{}).Authorization,body});
  await new Promise(r=>setTimeout(r,300));
  const js=(o,s)=>new Response(JSON.stringify(o),{status:s||200});
  if(window.__fnMode==='loi') return js({loi:'Chỉ chủ app được tạo bản tin'},403);
  if(window.__fnMode==='404') return js({},404);
  const d=new Date(Date.now()+7*3600000).toISOString().slice(0,10);
  const n=%s; n.ngay=d;
  const D=window.__DB.ban_tin; const cu=D.find(r=>r.ngay===d);
  if(cu&&!body.ep) return js({ngay:d,tao_moi:false,so_tin:cu.noi_dung.tin.length,dung_ai:cu.noi_dung.dung_ai,da_gui:!!cu.telegram_luc});
  if(cu){cu.noi_dung=n;cu.tao_luc=new Date().toISOString();} else D.push({ngay:d,noi_dung:n,tao_luc:new Date().toISOString(),telegram_luc:null,loi:null});
  __luuDb();
  return js({ngay:d,tao_moi:true,so_tin:n.tin.length,dung_ai:true,da_gui:false});
 }
 return __real(u,i);
};
"""
MOI = nd(ngay(0), [tin('Thế giới', 'BBC', 'Tin mới tạo từ nút bấm', 'Tóm tắt của bản vừa tạo.', 'https://bbc.co.uk/moi'),
                   tin('Thể thao', 'VnExpress', 'Tin thể thao mới tạo', 'Chi tiết.', 'https://vnexpress.net/moi')])

def dung_fake(bt): return FAKE % (json.dumps(YT), json.dumps(bt), json.dumps(CATS), json.dumps(MOI))

ok_all = True
def check(ten, cond, ct=""):
    global ok_all
    ok_all &= bool(cond); say(('  ĐẠT  ' if cond else '  HỎNG '), ten + ('' if cond or not ct else '  -> ' + str(ct)))
def tbl(pg, t): return pg.evaluate("t=>window.__DB[t]", t)
def shot(pg, name): pg.screenshot(path=os.path.join(OUT, name))

def mo(browser, bt=None, **kw):
    ctx = browser.new_context(**kw); pg = ctx.new_page(); errs = []
    pg.on("pageerror", lambda e: errs.append(str(e)))
    dlg = []
    pg.on("dialog", lambda d: (dlg.append(d.message), d.accept()))
    fk = dung_fake(BT if bt is None else bt)
    pg.route("**/@supabase/supabase-js@2", lambda r: r.fulfill(body=fk, content_type="application/javascript"))
    pg.goto("file:///" + ROOT.replace("\\", "/") + "/index.html")
    pg.wait_for_selector("#app:not([hidden])")
    return ctx, pg, errs, dlg

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx, pg, errs, dlg = mo(b, viewport=dict(width=1200, height=900))
    say("1) Mở trang Bản tin trên máy tính")
    check("Menu trái có mục 'Bản tin'", pg.locator(".nav a[data-p=tin]").count() == 1 and 'Bản tin' in pg.locator(".nav a[data-p=tin]").inner_text())
    pg.click(".nav a[data-p=tin]"); pg.wait_for_selector("#btView .bt-item"); pg.wait_for_timeout(200)
    check("Mặc định hiện bản tin mới nhất (hôm nay) + danh sách 3 ngày để xem lại", pg.locator("#btNgay option").count() == 3 and pg.input_value("#btNgay") == ngay(0))
    check("Đầu trang: 'Đã gửi qua Telegram lúc 08:00' + 8 tin", pg.locator(".bt-tg").first.inner_text().count('08:00') == 1 and '8 tin' in pg.locator(".bt-tg").first.inner_text())
    box = pg.locator("#btView").inner_text()
    check("Phần đầu: lịch hôm nay (có cả ngày + giờ), việc trễ hạn, ý tưởng để lâu", 'Sinh nhật mẹ' in box and '09:00 – 10:00' in box and 'Nộp báo cáo thuế' in box and 'Làm kênh review đồ bếp — 20 ngày' in box)
    check("Tin nhóm theo 7 chủ đề, mỗi tin có tên báo", pg.locator(".bt-topic").count() == 7 and pg.locator(".bt-item .src a").count() >= 7)
    a0 = pg.locator(".bt-item .src a").first
    check("Link tên báo mở tab mới, rel có noopener", a0.get_attribute('target') == '_blank' and 'noopener' in a0.get_attribute('rel') and a0.get_attribute('href') == 'https://vnexpress.net/a-1')
    check("Tin gộp ghi 'cũng đưa tin: Tuổi Trẻ'", 'cũng đưa tin: Tuổi Trẻ' in box)
    check("Dòng cuối: 'không lấy được tin từ: NHK World (Thế giới)'", 'Hôm nay không lấy được tin từ: NHK World (Thế giới)' in box)
    check("XSS: thẻ <img>/<script> trong tin chỉ hiện thành chữ, không chạy", pg.evaluate("window.__xss") is None and pg.locator("#btView img").count() == 0 and pg.locator("#btView script").count() == 0 and '<img src=x' in box and '<b>quan trọng</b>' in box)
    check("XSS: link javascript: không thành thẻ <a> bấm được", pg.locator("#btView a[href^=javascript]").count() == 0 and pg.locator(".bt-item:has-text('Giá vàng') .src a").count() == 0)
    check("Tin có nút '💡 Lưu thành ý tưởng' (8 nút)", pg.locator("[data-bt-luu]").count() == 8)
    shot(pg, "01-ban-tin-may-tinh.png")

    say("2) Xem lại ngày trước")
    pg.select_option("#btNgay", ngay(1)); pg.wait_for_timeout(200)
    t = pg.locator("#btView").inner_text()
    check("Ngày hôm qua: chưa gửi Telegram + cảnh báo chưa dịch + tin Anh có nhãn 'tiếng Anh'", 'Chưa gửi qua Telegram' in t and 'chưa dịch/tóm tắt được' in t and pg.locator(".bt-item:has-text('Germany') .tag").count() == 1)
    check("Ngày hôm qua: phần đầu rỗng hiện 'Hôm nay không có lịch'", 'Hôm nay không có lịch' in t and 'Không có việc trễ' in t)
    shot(pg, "02-ban-tin-hom-qua-tieng-anh.png")
    pg.select_option("#btNgay", ngay(2)); pg.wait_for_timeout(200)
    check("Ngày kia: chỉ 1 tin", pg.locator(".bt-item").count() == 1)
    pg.select_option("#btNgay", ngay(0)); pg.wait_for_timeout(200)

    say("3) Lưu thành ý tưởng")
    it = pg.locator(".bt-item:has-text('Quốc hội thông qua')")
    it.locator("[data-bt-luu]").click(); pg.wait_for_timeout(400)
    ys = [r for r in tbl(pg, 'y_tuong') if r.get('link') == 'https://vnexpress.net/a-1']
    check("Thêm 1 dòng vào y_tuong: tiêu đề, ghi chú=tóm tắt, nhãn 'từ bản tin', nguồn=tên báo, link gốc", len(ys) == 1 and ys[0]['tieu_de'] == 'Quốc hội thông qua luật đất đai sửa đổi' and ys[0]['ghi_chu'].startswith('Luật có hiệu lực') and ys[0]['nhan'] == ['từ bản tin'] and ys[0]['nguon'] == 'VnExpress' and ys[0]['trang_thai'] == 'chua_lam', json.dumps(ys, ensure_ascii=False))
    check("Nút đổi thành '✓ Đã lưu' (không còn nút lưu cho tin đó)", '✓ Đã lưu' in it.inner_text() and it.locator("[data-bt-luu]").count() == 0)
    pg.locator(".bt-item:has-text('Bộ Y tế') [data-bt-luu]").click(); pg.wait_for_timeout(300)
    pg.locator(".bt-item:has-text('Giá vàng') [data-bt-luu]").click(); pg.wait_for_timeout(300)
    gv = [r for r in tbl(pg, 'y_tuong') if r['tieu_de'] == 'Giá vàng trong nước giảm nhẹ']
    check("Tin có link không hợp lệ (javascript:) vẫn lưu được nhưng link = rỗng (không lưu link độc)", len(gv) == 1 and gv[0]['link'] is None)
    pg.click(".nav a[data-p=y]"); pg.wait_for_timeout(300)
    check("Kho ý tưởng có thẻ mới kèm nhãn #từ bản tin", pg.locator(".card:has-text('Quốc hội thông qua') .tag:has-text('từ bản tin')").count() == 1)
    shot(pg, "03-kho-y-tuong-co-the-tu-ban-tin.png")
    pg.reload(); pg.wait_for_selector("#app:not([hidden])"); pg.click(".nav a[data-p=tin]"); pg.wait_for_selector("#btView .bt-item"); pg.wait_for_timeout(200)
    check("Tải lại trang: tin đã lưu vẫn hiện '✓ Đã lưu' (nhớ theo link)", '✓ Đã lưu' in pg.locator(".bt-item:has-text('Quốc hội thông qua')").inner_text())
    pg.evaluate("window.__luuLoi=true"); pg.locator(".bt-item:has-text('Premier') [data-bt-luu]").click(); pg.wait_for_timeout(300)
    check("Lưu lỗi: có thông báo, nút vẫn bấm lại được", 'Lưu lỗi' in pg.inner_text("#toast") and pg.locator(".bt-item:has-text('Premier') [data-bt-luu]").is_enabled())
    pg.evaluate("window.__luuLoi=false")

    say("4) Nút 'Tạo bản tin hôm nay' khi đã có bản hôm nay")
    check("Nút đổi chữ thành 'Tạo lại bản tin hôm nay'", pg.inner_text("#btTao") == 'Tạo lại bản tin hôm nay')
    pg.click("#btTao"); pg.wait_for_timeout(100)
    check("Có hỏi xác nhận trước khi tạo lại; đang tạo thì nút bị khoá", any('Tạo lại' in m for m in dlg) and pg.locator("#btTao").is_disabled())
    pg.wait_for_selector("#btTao:not([disabled])"); pg.wait_for_timeout(300)
    goi = pg.evaluate("window.__goi")
    check("Gọi function ban-tin-gui với token đăng nhập + chi_tao:true + ep:true (không gửi Telegram)", len(goi) == 1 and goi[0]['auth'] == 'Bearer TOKEN-GIA' and goi[0]['body'] == dict(chi_tao=True, ep=True), json.dumps(goi))
    check("Hiện bản mới tạo (2 tin)", pg.locator(".bt-item").count() == 2 and 'Tin mới tạo từ nút bấm' in pg.locator("#btView").inner_text())
    pg.evaluate("window.__fnMode='loi'"); pg.click("#btTao"); pg.wait_for_selector("#btTao:not([disabled])"); pg.wait_for_timeout(200)
    check("Function báo lỗi: hiện đúng thông báo, trang không hỏng", 'Chỉ chủ app' in pg.inner_text("#toast") and pg.locator(".bt-item").count() == 2)
    pg.evaluate("window.__fnMode='404'"); pg.click("#btTao"); pg.wait_for_selector("#btTao:not([disabled])"); pg.wait_for_timeout(200)
    check("Function chưa deploy (404): thông báo dễ hiểu", 'chưa deploy' in pg.inner_text("#toast"))
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS (máy tính): %s' % errs, not errs)

    say("5) Mất mạng: xem bản đã lưu, chỉ đọc")
    pg.evaluate("window.__fnMode='ok'; localStorage.setItem('__btloi','1')")
    pg.reload(); pg.wait_for_selector("#app:not([hidden])"); pg.click(".nav a[data-p=tin]"); pg.wait_for_selector("#btView .bt-item"); pg.wait_for_timeout(300)
    check("Vẫn xem được bản tin đã lưu trong máy, có dòng 'chỉ đọc'", 'chỉ đọc' in pg.locator(".bt-tg").first.inner_text() and pg.locator(".bt-item").count() >= 1)
    n0 = len(tbl(pg, 'y_tuong'))
    pg.locator("[data-bt-luu]").first.click(); pg.wait_for_timeout(200)
    check("Mất mạng: bấm Lưu thành ý tưởng bị chặn (không thêm gì)", len(tbl(pg, 'y_tuong')) == n0 and 'chỉ đọc' in pg.inner_text("#toast"))
    shot(pg, "04-mat-mang-chi-doc.png")
    ctx.close()

    say("6) Chưa có bản tin hôm nay -> bấm Tạo")
    ctx, pg, errs, dlg = mo(b, bt=[BT[1], BT[2]], viewport=dict(width=1200, height=800))
    pg.click(".nav a[data-p=tin]"); pg.wait_for_selector("#btView .bt-item"); pg.wait_for_timeout(200)
    check("Chưa có hôm nay: nút ghi 'Tạo bản tin hôm nay', mặc định hiện ngày mới nhất đang có", pg.inner_text("#btTao") == 'Tạo bản tin hôm nay' and pg.input_value("#btNgay") == ngay(1))
    pg.click("#btTao"); pg.wait_for_selector("#btTao:not([disabled])"); pg.wait_for_timeout(300)
    goi = pg.evaluate("window.__goi")
    check("Không hỏi xác nhận, gọi với ep:false; tự chuyển sang bản hôm nay", not dlg and goi[0]['body'] == dict(chi_tao=True, ep=False) and pg.input_value("#btNgay") == ngay(0) and pg.locator(".bt-item").count() == 2)
    ctx.close()

    say("7) Chưa có bản tin nào")
    ctx, pg, errs, dlg = mo(b, bt=[], viewport=dict(width=1200, height=800))
    pg.click(".nav a[data-p=tin]"); pg.wait_for_timeout(500)
    check("Hiện hướng dẫn thân thiện, không lỗi", 'Chưa có bản tin nào' in pg.inner_text("#btView") and pg.locator("#btNgay").is_hidden())
    shot(pg, "05-chua-co-ban-tin.png")
    ctx.close()

    say("8) Điện thoại (390x800)")
    ctx, pg, errs, dlg = mo(b, viewport=dict(width=390, height=800), has_touch=True, is_mobile=True, device_scale_factor=2)
    check("Thanh menu dưới có 4 mục: Lịch / Ý tưởng / Bản tin / Cài đặt", pg.locator("#duoi a").count() == 4 and 'Bản tin' in pg.locator("#duoi a[data-p=tin]").inner_text())
    pg.tap("#duoi a[data-p=tin]"); pg.wait_for_selector("#btView .bt-item"); pg.wait_for_timeout(300)
    check("Mở được Bản tin từ thanh dưới (mục sáng lên)", pg.locator("#p-tin.on").count() == 1 and pg.locator("#duoi a[data-p=tin].on").count() == 1)
    check("Không tràn ngang trên điện thoại", pg.evaluate("document.querySelector('main').scrollWidth <= document.querySelector('main').clientWidth + 1"))
    shot(pg, "06-ban-tin-dien-thoai.png")
    pg.evaluate("document.querySelector('main').scrollTo(0, 700)"); pg.wait_for_timeout(200)
    shot(pg, "07-ban-tin-dien-thoai-cuon.png")
    pg.tap("[data-bt-luu] >> nth=0"); pg.wait_for_timeout(400)
    check("Lưu thành ý tưởng bằng cảm ứng chạy được", len(tbl(pg, 'y_tuong')) == 2)
    errs = [x for x in errs if 'ServiceWorker' not in x]; check('Không có lỗi JS (điện thoại): %s' % errs, not errs)
    ctx.close(); b.close()
say("TẤT CẢ ĐẠT" if ok_all else "CÓ LỖI")
sys.exit(0 if ok_all else 1)
