// Cấu hình nguồn tin cho bản tin sáng (giai đoạn 2.8). Đã kiểm chứng ngày 2026-11-26 bằng tools/kiem_rss.py
// (bằng chứng: docs/bang-chung/2.8/kiem-rss.txt, bảng chốt: docs/bang-chung/2.8/nguon-chot.md).
// Muốn thêm/bớt báo: chỉ sửa file này.

export const CHU_DE = {
  thoi_su: 'Thời sự trong nước',
  the_gioi: 'Thế giới',
  kinh_te: 'Kinh tế – tài chính',
  cong_nghe: 'Công nghệ – AI',
  tmdt: 'Kinh doanh online / TMĐT',
  suc_khoe: 'Sức khoẻ',
  the_thao: 'Thể thao',
} as const;
export type MaChuDe = keyof typeof CHU_DE;

export type Nguon = {
  bao: string;
  chu_de: MaChuDe;
  url: string;
  // true: tin của mục kinh tế này mà có từ khoá TMĐT (TMDT_TU_KHOA) thì xếp vào "Kinh doanh online / TMĐT" thay vì "Kinh tế".
  tmdt?: boolean;
};

// Không có báo nào chuyên mục TMĐT riêng có RSS => lọc theo từ khoá trong các mục kinh tế.
export const TMDT_TU_KHOA = /thương mại điện tử|sàn điện tử|tmđt|shopee|lazada|tiktok shop|\btiki\b|\btemu\b|\bshein\b|bán hàng (online|trực tuyến)|kinh doanh (online|trực tuyến)|mua sắm (online|trực tuyến)|livestream|nhà bán hàng|người bán hàng|giao hàng|ví điện tử|tiktok|nền tảng thương mại|bán lẻ trực tuyến|e-?commerce|online (shopping|retail)|amazon\.com|amazon (prime|seller|marketplace)|alibaba|\bebay\b/i;

export const NGUON: Nguon[] = [
  // VnExpress (mục "kinh-doanh" dùng cho cả Kinh tế lẫn TMĐT qua bộ lọc từ khoá)
  { bao: 'VnExpress', chu_de: 'thoi_su', url: 'https://vnexpress.net/rss/thoi-su.rss' },
  { bao: 'VnExpress', chu_de: 'the_gioi', url: 'https://vnexpress.net/rss/the-gioi.rss' },
  { bao: 'VnExpress', chu_de: 'kinh_te', url: 'https://vnexpress.net/rss/kinh-doanh.rss', tmdt: true },
  { bao: 'VnExpress', chu_de: 'cong_nghe', url: 'https://vnexpress.net/rss/so-hoa.rss' },
  { bao: 'VnExpress', chu_de: 'suc_khoe', url: 'https://vnexpress.net/rss/suc-khoe.rss' },
  { bao: 'VnExpress', chu_de: 'the_thao', url: 'https://vnexpress.net/rss/the-thao.rss' },
  // Tuổi Trẻ
  { bao: 'Tuổi Trẻ', chu_de: 'thoi_su', url: 'https://tuoitre.vn/rss/thoi-su.rss' },
  { bao: 'Tuổi Trẻ', chu_de: 'the_gioi', url: 'https://tuoitre.vn/rss/the-gioi.rss' },
  { bao: 'Tuổi Trẻ', chu_de: 'kinh_te', url: 'https://tuoitre.vn/rss/kinh-doanh.rss', tmdt: true },
  { bao: 'Tuổi Trẻ', chu_de: 'cong_nghe', url: 'https://tuoitre.vn/rss/nhip-song-so.rss' },
  { bao: 'Tuổi Trẻ', chu_de: 'suc_khoe', url: 'https://tuoitre.vn/rss/suc-khoe.rss' },
  { bao: 'Tuổi Trẻ', chu_de: 'the_thao', url: 'https://tuoitre.vn/rss/the-thao.rss' },
  // Thanh Niên
  { bao: 'Thanh Niên', chu_de: 'thoi_su', url: 'https://thanhnien.vn/rss/thoi-su.rss' },
  { bao: 'Thanh Niên', chu_de: 'the_gioi', url: 'https://thanhnien.vn/rss/the-gioi.rss' },
  { bao: 'Thanh Niên', chu_de: 'kinh_te', url: 'https://thanhnien.vn/rss/kinh-te.rss', tmdt: true },
  { bao: 'Thanh Niên', chu_de: 'cong_nghe', url: 'https://thanhnien.vn/rss/cong-nghe.rss' },
  { bao: 'Thanh Niên', chu_de: 'suc_khoe', url: 'https://thanhnien.vn/rss/suc-khoe.rss' },
  { bao: 'Thanh Niên', chu_de: 'the_thao', url: 'https://thanhnien.vn/rss/the-thao.rss' },
  // VOV (đường dẫn cũ dạng chinh-tri-212.rss đã chết; đường dẫn mới không có số, lấy từ https://vov.vn/rss.html)
  { bao: 'VOV', chu_de: 'thoi_su', url: 'https://vov.vn/rss/chinh-tri.rss' },
  { bao: 'VOV', chu_de: 'thoi_su', url: 'https://vov.vn/rss/xa-hoi.rss' },
  { bao: 'VOV', chu_de: 'the_gioi', url: 'https://vov.vn/rss/the-gioi.rss' },
  { bao: 'VOV', chu_de: 'kinh_te', url: 'https://vov.vn/rss/kinh-te.rss', tmdt: true },
  { bao: 'VOV', chu_de: 'cong_nghe', url: 'https://vov.vn/rss/cong-nghe.rss' },
  { bao: 'VOV', chu_de: 'suc_khoe', url: 'https://vov.vn/rss/suc-khoe.rss' },
  { bao: 'VOV', chu_de: 'the_thao', url: 'https://vov.vn/rss/the-thao.rss' },
  // Báo Chính phủ (đuôi .rss nằm ngay sau tên mục, không có /rss/)
  { bao: 'Báo Chính phủ', chu_de: 'thoi_su', url: 'https://baochinhphu.vn/chinh-tri.rss' },
  { bao: 'Báo Chính phủ', chu_de: 'thoi_su', url: 'https://baochinhphu.vn/thoi-su.rss' },
  { bao: 'Báo Chính phủ', chu_de: 'kinh_te', url: 'https://baochinhphu.vn/kinh-te.rss', tmdt: true },
  { bao: 'Báo Chính phủ', chu_de: 'cong_nghe', url: 'https://baochinhphu.vn/khoa-hoc-cong-nghe.rss' },
  { bao: 'Báo Chính phủ', chu_de: 'suc_khoe', url: 'https://baochinhphu.vn/y-te.rss' },
  // BBC
  { bao: 'BBC', chu_de: 'the_gioi', url: 'https://feeds.bbci.co.uk/news/world/rss.xml' },
  { bao: 'BBC', chu_de: 'kinh_te', url: 'https://feeds.bbci.co.uk/news/business/rss.xml', tmdt: true },
  { bao: 'BBC', chu_de: 'cong_nghe', url: 'https://feeds.bbci.co.uk/news/technology/rss.xml' },
  { bao: 'BBC', chu_de: 'suc_khoe', url: 'https://feeds.bbci.co.uk/news/health/rss.xml' },
  { bao: 'BBC', chu_de: 'the_thao', url: 'https://feeds.bbci.co.uk/sport/rss.xml' },
  // The Guardian
  { bao: 'The Guardian', chu_de: 'the_gioi', url: 'https://www.theguardian.com/world/rss' },
  { bao: 'The Guardian', chu_de: 'kinh_te', url: 'https://www.theguardian.com/business/rss', tmdt: true },
  { bao: 'The Guardian', chu_de: 'cong_nghe', url: 'https://www.theguardian.com/technology/rss' },
  { bao: 'The Guardian', chu_de: 'suc_khoe', url: 'https://www.theguardian.com/society/health/rss' },
  { bao: 'The Guardian', chu_de: 'the_thao', url: 'https://www.theguardian.com/sport/rss' },
  // DW (chỉ còn 2 mục; rss-en-sci và rss-en-sport không còn trả XML)
  { bao: 'DW', chu_de: 'the_gioi', url: 'https://rss.dw.com/xml/rss-en-world' },
  { bao: 'DW', chu_de: 'kinh_te', url: 'https://rss.dw.com/xml/rss-en-bus', tmdt: true },
  // NHK World: ĐÃ BỎ — RSS tiếng Anh không còn (mọi đường dẫn /nhkworld/en/news/feeds/ trả 404);
  // chỉ còn bản tiếng Nhật www3.nhk.or.jp/rss/news/cat*.xml và all.json, đều ngừng cập nhật từ tháng 8–9/2026.
];

export const GIO_TOI_DA = 36; // chỉ lấy tin trong 36 giờ gần nhất
export const HAN_CHOT_MS = 8000; // mỗi nguồn tối đa 8 giây
export const TOI_DA_MOI_NGUON = 15; // mỗi RSS chỉ giữ 15 tin mới nhất (tránh JSON quá lớn)
export const NGUONG_TRUNG_TIEU_DE = 0.6; // độ giống tiêu đề (Jaccard theo từ) từ mức này coi là trùng
