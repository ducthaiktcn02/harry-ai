// Bộ kiểm "ban-tin-lay" bằng RSS giả (tools/mau_rss/). Chạy qua: py -3.12 tools/thu_ban_tin_gia.py (cần deno).
// In ra JSON: [{ten, dat, chi_tiet}]. Không gọi mạng.
import { chuanHoaLink, chuanHoaNguon, docRss, doGiong, giaiMaKyTu, gopTrung, layTatCa, linkSach, tuCuaTieuDe } from '../supabase/functions/ban-tin-lay/loi.ts';
import type { Nguon } from '../supabase/functions/ban-tin-lay/nguon.ts';
import { CHU_DE } from '../supabase/functions/ban-tin-lay/nguon.ts';

const dir = new URL('./mau_rss/', import.meta.url);
const doc = (f: string) => Deno.readTextFileSync(new URL(f, dir));
const rss2 = doc('rss2.xml'), atom = doc('atom.xml'), hong = doc('hong.xml'), html = doc('html.xml'), trong = doc('trong.xml');
const NOW = Date.parse('2026-11-26T01:00:00Z');
const kq: { ten: string; dat: boolean; chi_tiet: string }[] = [];
const kiem = (ten: string, dieuKien: boolean, chi_tiet = '') => kq.push({ ten, dat: !!dieuKien, chi_tiet: String(chi_tiet) });
const nA: Nguon = { bao: 'Báo Giả A', chu_de: 'kinh_te', url: 'https://a.example/rss', tmdt: true };
const nA2: Nguon = { ...nA, tmdt: false };
const nB: Nguon = { bao: 'Báo Giả B', chu_de: 'kinh_te', url: 'https://b.example/atom', tmdt: true };

// Parse RSS 2.0
const a = docRss(rss2);
kiem('RSS 2.0: đọc đủ 5 mục', a.length === 5, `${a.length} mục`);
kiem('RSS 2.0: tiêu đề CDATA + mô tả cắt sạch HTML, giải mã &agrave;', a[0].tieu_de === 'Giá vàng trong nước tăng mạnh phiên sáng nay' && a[0].mo_ta === 'Giá vàng SJC tăng 500.000 đồng mỗi lượng.', JSON.stringify(a[0].mo_ta));
kiem('RSS 2.0: tiêu đề có &amp; được giải mã', a[3].tieu_de === 'Bão số 9 đổ bộ miền Trung & Tây Nguyên', a[3].tieu_de);
kiem('RSS 2.0: pubDate RFC822 +0700 đổi đúng sang UTC', a[0].t === Date.parse('2026-11-25T20:00:00Z'), String(a[0].t));
kiem('RSS: ngày kiểu MM/DD/YYYY h:mm:ss AM (Tuổi Trẻ/Báo Chính phủ) hiểu là giờ VN', a[3].t === Date.parse('2026-11-26T00:23:00Z'), String(a[3].t));
kiem('RSS: dc:date ISO được đọc', a[4].t === Date.parse('2026-11-25T22:00:00Z'), String(a[4].t));
kiem('RSS: mục không có ngày -> t=null', a[2].t === null);
// Atom
const b = docRss(atom);
kiem('Atom: đọc đủ 4 mục', b.length === 4, `${b.length} mục`);
kiem('Atom: lấy link rel=alternate (không lấy rel=self)', b[0].link === 'https://www.b.example/vang-tang-manh-phien-sang', b[0].link);
kiem('Atom: summary HTML thoát (&lt;p&gt;) cũng được cắt sạch', b[0].mo_ta === 'Bản tin của báo B về giá vàng.', b[0].mo_ta);
kiem('Atom: <published> có múi giờ +07:00', b[1].t === Date.parse('2026-11-25T16:00:00Z'), String(b[1].t));
kiem('Atom: link self-closing <link href="..."/> đọc được', b[1].link === 'https://b.example/bao-so-9-do-bo', b[1].link);
// Lọc 36h + cắt 300
const ca = chuanHoaNguon(a, nA2, NOW);
kiem('Lọc 36 giờ: bỏ tin cũ (23/11) và tin không rõ ngày -> còn 3', ca.length === 3 && !ca.some((t) => /cũ|không có ngày/i.test(t.tieu_de)), ca.map((t) => t.tieu_de).join(' | '));
kiem('Mô tả dài bị cắt ≤ 300 ký tự và có …', ca.every((t) => Array.from(t.mo_ta).length <= 300) && ca.some((t) => t.mo_ta.endsWith('…') && Array.from(t.mo_ta).length > 250), ca.map((t) => Array.from(t.mo_ta).length).join(','));
kiem('Mô tả không còn thẻ HTML hay &xxx; thô', ca.every((t) => !/[<>]|&[a-z]+;/.test(t.mo_ta)));
kiem('Đủ trường chuẩn hoá', ca.every((t) => t.chu_de && t.bao && t.tieu_de && t.link && typeof t.mo_ta === 'string' && /^\d{4}-\d\d-\d\dT/.test(t.thoi_gian)));
kiem('Link đưa ra đã bỏ utm_/fbclid/#', ca.some((t) => t.link === 'https://a.example/gia-vang-tang'), ca.map((t) => t.link).join(' '));
// Chủ đề TMĐT
const caT = chuanHoaNguon(a, nA, NOW);
kiem('Từ khoá TMĐT (Shopee) -> chủ đề "Kinh doanh online / TMĐT" khi nguồn có tmdt', caT.find((t) => /Shopee/.test(t.tieu_de))?.chu_de === CHU_DE.tmdt);
kiem('Tin kinh tế thường vẫn ở "Kinh tế – tài chính"', caT.find((t) => /vàng/.test(t.tieu_de))?.chu_de === CHU_DE.kinh_te);
kiem('Nguồn không bật tmdt giữ nguyên chủ đề', ca.every((t) => t.chu_de === CHU_DE.kinh_te));
// Gộp trùng
kiem('Chuẩn hoá link: bỏ utm/fbclid/#/www/dấu / cuối', chuanHoaLink('https://WWW.A.example/gia-vang-tang/?utm_source=x&fbclid=1#top') === 'a.example/gia-vang-tang' && chuanHoaLink('https://a.example/gia-vang-tang') === 'a.example/gia-vang-tang');
const ls = linkSach('https://x.vn/bai?id=5&utm_campaign=z&at_medium=RSS#a');
kiem('Link sạch giữ tham số thật (id=5), bỏ tham số theo dõi', ls === 'https://x.vn/bai?id=5', ls);
const mk = (bao: string, tieu_de: string, link: string) => ({ chu_de: CHU_DE.kinh_te, bao, tieu_de, link, mo_ta: '', thoi_gian: '2026-11-26T00:00:00.000Z' });
const g1 = gopTrung([mk('A', 'Tin hoàn toàn khác nhau số một', 'https://a.vn/x?utm_source=1'), mk('B', 'Chủ đề không liên quan chút nào hết', 'https://www.a.vn/x/')]);
kiem('Gộp trùng theo link (khác utm/www/dấu /) dù tiêu đề khác', g1.tin.length === 1 && g1.trung === 1 && g1.tin[0].trung_voi?.[0] === 'B', JSON.stringify(g1.tin));
const g2 = gopTrung([mk('A', 'Giá vàng trong nước tăng mạnh phiên sáng nay', 'https://a/1'), mk('B', 'Giá vàng trong nước tăng mạnh trong phiên sáng', 'https://b/2'), mk('C', 'Giá vàng thế giới giảm nhẹ khi đồng USD mạnh lên', 'https://c/3')]);
kiem('Gộp trùng theo tiêu đề giống (≥ 0.6): giữ bản đầu, ghi trung_voi, KHÔNG gộp nhầm tin khác ý', g2.tin.length === 2 && g2.tin[0].bao === 'A' && g2.tin[0].trung_voi?.join() === 'B' && g2.tin[1].bao === 'C', JSON.stringify(g2.tin.map((t) => [t.bao, t.trung_voi])));
const tdA = tuCuaTieuDe('Giá vàng trong nước tăng mạnh phiên sáng nay');
const giongDuoi = doGiong(tdA, tuCuaTieuDe('Giá vàng trong nước tăng mạnh trong phiên sáng'));
const giongKhac = doGiong(tdA, tuCuaTieuDe('Giá vàng thế giới giảm nhẹ khi đồng USD mạnh lên'));
kiem(`Độ giống: cùng ý = ${giongDuoi.toFixed(2)} (>=0.6), khác ý = ${giongKhac.toFixed(2)} (<0.3)`, giongDuoi >= 0.6 && giongKhac < 0.3);
kiem('Tiêu đề quá ngắn (<4 từ) không so khớp mờ', gopTrung([mk('A', 'Tin nóng', 'https://a/1'), mk('B', 'Tin nóng', 'https://b/2')]).tin.length === 2);
// layTatCa với nguồn lỗi
const ban: Record<string, () => Promise<string>> = {
  'https://a.example/rss': () => Promise.resolve(rss2),
  'https://b.example/atom': () => Promise.resolve(atom),
  'https://c.example/503': () => Promise.reject(new Error('HTTP 503')),
  'https://d.example/treo': () => new Promise<string>(() => { /* không bao giờ trả lời */ }),
  'https://e.example/hong': () => Promise.resolve(hong),
  'https://f.example/html': () => Promise.resolve(html),
  'https://g.example/trong': () => Promise.resolve(trong),
};
const tai = (u: string) => ban[u]();
const ds: Nguon[] = [
  nA, nB,
  { bao: 'Báo Lỗi 503', chu_de: 'the_gioi', url: 'https://c.example/503' },
  { bao: 'Báo Treo', chu_de: 'thoi_su', url: 'https://d.example/treo' },
  { bao: 'Báo XML Hỏng', chu_de: 'suc_khoe', url: 'https://e.example/hong' },
  { bao: 'Báo Trả HTML', chu_de: 'the_thao', url: 'https://f.example/html' },
  { bao: 'Báo Trống', chu_de: 'cong_nghe', url: 'https://g.example/trong' },
];
const t0 = Date.now();
const r = await layTatCa(ds, tai, NOW, 150);
const giay = Date.now() - t0;
kiem('Nguồn treo bị cắt đúng hạn (không treo cả bản)', giay < 2000, `${giay} ms`);
kiem('Có tên báo lỗi: 503, treo, XML hỏng, trả HTML', ['Báo Lỗi 503', 'Báo Treo', 'Báo XML Hỏng', 'Báo Trả HTML'].every((n) => r.loi.some((x) => x.startsWith(n))), JSON.stringify(r.loi));
kiem('Nguồn rỗng hợp lệ (RSS không có tin) KHÔNG bị coi là lỗi', !r.loi.some((x) => x.startsWith('Báo Trống')) && r.dem.nguon_loi === 4 && r.dem.nguon_ok === 3, JSON.stringify(r.dem));
kiem('Lý do lỗi được ghi cho từng nguồn', r.loi_chi_tiet.length === 4 && r.loi_chi_tiet.every((x) => x.ly_do && x.url), r.loi_chi_tiet.map((x) => x.ly_do).join(' | '));
kiem('Bản vẫn ra tin từ các nguồn tốt', r.dem.tong > 0 && r.tin[CHU_DE.kinh_te].length > 0, JSON.stringify(r.dem.theo_chu_de));
kiem('Gộp trùng chạy trong layTatCa (giá vàng A+B chỉ còn 1)', r.tin[CHU_DE.kinh_te].filter((t) => /giá vàng trong nước/i.test(t.tieu_de)).length === 1 && r.dem.da_gop_trung >= 2, `trùng=${r.dem.da_gop_trung}`);
kiem('Tin gộp ghi trung_voi: Báo Giả B', r.tin[CHU_DE.kinh_te].find((t) => /giá vàng trong nước/i.test(t.tieu_de))?.trung_voi?.includes('Báo Giả B') === true);
kiem('Đủ 7 chủ đề, chủ đề rỗng là mảng rỗng', Object.values(CHU_DE).every((t) => Array.isArray(r.tin[t])) && r.tin[CHU_DE.suc_khoe].length === 0 && r.tin[CHU_DE.the_thao].length === 0, Object.keys(r.tin).join(','));
kiem('Tin TMĐT tách đúng chủ đề trong bản tổng hợp', r.tin[CHU_DE.tmdt].length === 1 && /Shopee/.test(r.tin[CHU_DE.tmdt][0].tieu_de), JSON.stringify(r.tin[CHU_DE.tmdt].map((t) => t.tieu_de)));
kiem('Tin trong chủ đề xếp mới nhất trước', r.tin[CHU_DE.kinh_te].every((t, i, d) => i === 0 || d[i - 1].thoi_gian >= t.thoi_gian));
// Tất cả nguồn lỗi / không có nguồn
const r2 = await layTatCa(ds.slice(2, 6), tai, NOW, 100);
kiem('Mọi nguồn lỗi: vẫn trả kết quả, 7 chủ đề đều rỗng, ghi đủ 4 lỗi', r2.dem.tong === 0 && r2.loi.length === 4 && Object.values(r2.tin).every((x) => x.length === 0), JSON.stringify(r2.dem));
const r3 = await layTatCa([], tai, NOW);
kiem('Danh sách nguồn rỗng không lỗi', r3.dem.tong === 0 && Object.keys(r3.tin).length === 7);
// Ký tự đặc biệt
const gm = giaiMaKyTu('Ti&ecirc;n &#7849; &#x1EA9; AT&amp;T &unknown;');
kiem('Giải mã &ecirc; &#7849; &#x1EA9; &amp;, giữ nguyên thực thể lạ', gm === 'Tiên ẩ ẩ AT&T &unknown;', gm);
console.log(JSON.stringify(kq));
