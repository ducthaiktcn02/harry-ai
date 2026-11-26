"""Thử logic tính giờ nhắc (hàm cacLan + cửa sổ 10 phút) của Edge Function nhac-viec, chạy trong Chrome (máy không có Node/Deno).
Chạy: py -3.12 tools/thu_nhac_gia.py"""
import re, os, sys
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
s = open(os.path.join(ROOT, 'supabase/functions/nhac-viec/index.ts'), encoding='utf-8').read()
js = s[s.index('const VN'):s.index('const gio')]
js = re.sub(r"type Row = \{.*?\};\n", "", js, flags=re.S)
js = js.replace("(r: Row, from: number, to: number): number[]", "(r, from, to)").replace("const out: number[] = []", "const out = []").replace("(t: number)", "(t)")
# Lấy đúng đoạn vòng lặp gửi trong Deno.serve để thử chung công thức
js += """
function fire(r, now){const off=r.ca_ngay?8*3600000:0,nh=r.nhac_phut*60000;
 return cacLan(r,now-CUA_SO-off+nh,now-off+nh).filter(t=>{const d=t+off-nh;return d<=now&&d>now-CUA_SO}).map(t=>new Date(t).toISOString());}
const mk=(o)=>({lap:'none',lap_den:null,lap_ngoai:[],ca_ngay:false,...o});
const N=Date.parse('2026-11-27T01:00:00Z'); // 08:00 giờ VN
window.T=[
 ['Lẻ, nhắc 15p, giờ bắt đầu 08:15 -> gửi', fire(mk({bat_dau:'2026-11-27T01:15:00Z',nhac_phut:15}),N), 1],
 ['Lẻ, nhắc 15p, bắt đầu 09:15 -> chưa gửi', fire(mk({bat_dau:'2026-11-27T02:15:00Z',nhac_phut:15}),N), 0],
 ['Lẻ, nhắc 15p, đã trễ 30 phút -> không bù', fire(mk({bat_dau:'2026-11-27T01:15:00Z',nhac_phut:15}),N+30*60000), 0],
 ['Lẻ, lỡ 5 phút vẫn bù', fire(mk({bat_dau:'2026-11-27T01:15:00Z',nhac_phut:15}),N+5*60000), 1],
 ['Hằng ngày 08:00, đúng giờ', fire(mk({bat_dau:'2026-11-20T01:00:00Z',lap:'day',nhac_phut:0}),N), 1],
 ['Hằng tuần (T6) 09:00, trước 1 giờ', fire(mk({bat_dau:'2026-11-20T02:00:00Z',lap:'week',nhac_phut:60}),N), 1],
 ['Hằng tuần, hôm nay không phải ngày lặp', fire(mk({bat_dau:'2026-11-21T02:00:00Z',lap:'week',nhac_phut:60}),N), 0],
 ['Hằng tháng ngày 27, trước 1 giờ', fire(mk({bat_dau:'2026-09-27T02:00:00Z',lap:'month',nhac_phut:60}),N), 1],
 ['Hằng tháng ngày 31 (tháng 11 không có)', fire(mk({bat_dau:'2026-10-31T02:00:00Z',lap:'month',nhac_phut:60}),N), 0],
 ['Lần bị bỏ (ngoại lệ) -> không gửi', fire(mk({bat_dau:'2026-11-20T01:00:00Z',lap:'day',nhac_phut:0,lap_ngoai:['2026-11-27T01:00:00Z']}),N), 0],
 ['Lặp đã hết hạn (đến 26/11) -> không gửi', fire(mk({bat_dau:'2026-11-20T01:00:00Z',lap:'day',nhac_phut:0,lap_den:'2026-11-26'}),N), 0],
 ['Cả ngày 27/11, đúng giờ -> gửi lúc 8:00', fire(mk({bat_dau:'2026-11-26T17:00:00Z',ca_ngay:true,nhac_phut:0}),N), 1],
];
"""
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome'); pg = b.new_page(); pg.set_content('<html></html>')
    pg.evaluate(js.replace('window.T=', 'window.T=') ) if False else pg.add_script_tag(content=js)
    T = pg.evaluate('window.T'); b.close()
ok = True
for ten, got, want in T:
    good = len(got) == want; ok &= good
    print(('ĐẠT ' if good else 'HỎNG'), ten, got)
print('KẾT QUẢ:', 'TẤT CẢ ĐẠT' if ok else 'CÓ LỖI'); sys.exit(0 if ok else 1)
