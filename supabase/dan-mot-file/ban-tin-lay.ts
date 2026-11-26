// BẢN GỘP 1 FILE của ban-tin-lay (nguon.ts + loi.ts + index.ts), dán vào index.ts trên web Supabase.
// Đừng sửa tay: sinh bằng tools/gop_mot_file.py
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

// Phần "thuần" của ban-tin-lay (giai đoạn 2.8): đọc RSS/Atom, chuẩn hoá, lọc giờ, chọn chủ đề, gộp tin trùng.
// Không phụ thuộc Deno/mạng (trừ hàm layTatCa nhận sẵn một hàm tải) -> test được bằng tools/thu_ban_tin_gia.py.

export type Tin = {
  chu_de: string; bao: string; tieu_de: string; link: string; mo_ta: string; thoi_gian: string; trung_voi?: string[];
};
export type TinTho = { tieu_de: string; link: string; mo_ta: string; t: number | null };

// ---------- Giải mã ký tự đặc biệt ----------
const TEN_KY_TU: Record<string, string> = {
  amp: '&', lt: '<', gt: '>', quot: '"', apos: "'", nbsp: ' ', ndash: '–', mdash: '—', lsquo: '‘', rsquo: '’', ldquo: '“', rdquo: '”', hellip: '…',
  agrave: 'à', aacute: 'á', acirc: 'â', atilde: 'ã', egrave: 'è', eacute: 'é', ecirc: 'ê', igrave: 'ì', iacute: 'í',
  ograve: 'ò', oacute: 'ó', ocirc: 'ô', otilde: 'õ', ugrave: 'ù', uacute: 'ú', yacute: 'ý',
  Agrave: 'À', Aacute: 'Á', Acirc: 'Â', Atilde: 'Ã', Egrave: 'È', Eacute: 'É', Ecirc: 'Ê', Igrave: 'Ì', Iacute: 'Í',
  Ograve: 'Ò', Oacute: 'Ó', Ocirc: 'Ô', Otilde: 'Õ', Ugrave: 'Ù', Uacute: 'Ú', Yacute: 'Ý',
  auml: 'ä', ouml: 'ö', uuml: 'ü', Auml: 'Ä', Ouml: 'Ö', Uuml: 'Ü', szlig: 'ß', ccedil: 'ç', ntilde: 'ñ', aring: 'å', oslash: 'ø', aelig: 'æ',
  copy: '©', reg: '®', euro: '€', pound: '£', deg: '°',
};
export function giaiMaKyTu(s: string): string {
  return s.replace(/&(#x[0-9a-fA-F]+|#\d+|[A-Za-z][A-Za-z0-9]*);/g, (m, g: string) => {
    if (g[0] === '#') {
      const n = g[1] === 'x' || g[1] === 'X' ? parseInt(g.slice(2), 16) : parseInt(g.slice(1), 10);
      try { return n > 0 && n <= 0x10ffff ? String.fromCodePoint(n) : m; } catch (_) { return m; }
    }
    return Object.prototype.hasOwnProperty.call(TEN_KY_TU, g) ? TEN_KY_TU[g] : m;
  });
}

export function catHtml(s: string): string {
  return giaiMaKyTu(s.replace(/<(script|style)[\s\S]*?<\/\1>/gi, ' ').replace(/<[^>]*>/g, ' ')).replace(/\s+/g, ' ').trim();
}

export function catNgan(s: string, toiDa: number): string {
  const a = Array.from(s);
  return a.length <= toiDa ? s : a.slice(0, toiDa - 1).join('').replace(/\s+\S*$/, (m) => (m.trim().length > 12 ? m : '')).trimEnd() + '…';
}

// ---------- Đọc RSS 2.0 / Atom / RDF bằng regex ----------
function layTruong(khoi: string, ten: string): string | null {
  // tên có thể kèm tiền tố (dc:date, content:encoded); chỉ lấy thẻ không thuộc thẻ con lồng khác
  const re = new RegExp(`<(?:[A-Za-z0-9_]+:)?${ten}(?:\\s[^>]*)?>([\\s\\S]*?)</(?:[A-Za-z0-9_]+:)?${ten}>`, 'i');
  const m = re.exec(khoi);
  if (!m) return null;
  const cd = /^\s*<!\[CDATA\[([\s\S]*?)\]\]>\s*$/.exec(m[1]);
  return cd ? cd[1] : giaiMaKyTu(m[1]);
}

function layLinkAtom(khoi: string): string | null {
  let tot: string | null = null;
  for (const m of khoi.matchAll(/<link\b([^>]*?)\/?>/gi)) {
    const href = /href\s*=\s*["']([^"']+)["']/i.exec(m[1]);
    if (!href) continue;
    const rel = /rel\s*=\s*["']([^"']+)["']/i.exec(m[1]);
    if (!rel || rel[1] === 'alternate') return giaiMaKyTu(href[1]);
    tot = tot || giaiMaKyTu(href[1]);
  }
  return tot;
}

const RE_GIO_MDY = /^(\d{1,2})\/(\d{1,2})\/(\d{4})\s+(\d{1,2}):(\d{2})(?::(\d{2}))?\s*(AM|PM)$/i;
// Trả về mili giây UTC, hoặc null nếu không hiểu. Kiểu "11/26/2026 7:23:00 PM" (Tuổi Trẻ, Báo Chính phủ) là giờ Việt Nam (UTC+7).
export function docThoiGian(s: string | null): number | null {
  if (!s) return null;
  const x = s.trim();
  const m = RE_GIO_MDY.exec(x);
  if (m) {
    let h = parseInt(m[4], 10) % 12;
    if (m[7].toUpperCase() === 'PM') h += 12;
    return Date.UTC(+m[3], +m[1] - 1, +m[2], h, +m[5], m[6] ? +m[6] : 0) - 7 * 3600000;
  }
  const g = /^(.*?)\s*GMT([+-])(\d{1,2})$/.exec(x); // "Thu, 26 Nov 2026 19:15:49 GMT+7"
  const t = g ? Date.parse(`${g[1]} GMT`) - (g[2] === '+' ? 1 : -1) * +g[3] * 3600000 : Date.parse(x);
  return Number.isNaN(t) ? null : t;
}

export function docRss(xml: string): TinTho[] {
  if (typeof xml !== 'string' || !xml.trim()) throw new Error('Nguồn trả về rỗng');
  const goc = /<(rss|feed|rdf:RDF)\b/i.exec(xml);
  if (!goc) throw new Error('Không phải RSS/Atom (có thể là trang web)');
  if (!new RegExp(`</${goc[1]}>`, 'i').test(xml)) throw new Error('XML hỏng hoặc bị cắt cụt');
  const out: TinTho[] = [];
  for (const m of xml.matchAll(/<(item|entry)\b[^>]*>([\s\S]*?)<\/\1>/gi)) {
    const k = m[2];
    const tieu_de = catHtml(layTruong(k, 'title') || '');
    let link = (layTruong(k, 'link') || '').trim();
    if (!link || link.startsWith('<')) link = layLinkAtom(k) || (layTruong(k, 'guid') || '').trim();
    if (!tieu_de || !/^https?:\/\//i.test(link)) continue;
    const mo = catHtml(layTruong(k, 'description') || layTruong(k, 'summary') || layTruong(k, 'encoded') || layTruong(k, 'content') || '');
    const t = docThoiGian(layTruong(k, 'pubDate') || layTruong(k, 'published') || layTruong(k, 'updated') || layTruong(k, 'date'));
    out.push({ tieu_de, link, mo_ta: mo === tieu_de ? '' : mo, t });
  }
  return out;
}

// ---------- Chuẩn hoá link / tiêu đề để gộp trùng ----------
const THAM_SO_THEO_DOI = new Set(['fbclid', 'gclid', 'ref', 'ref_src', 'igshid', 'mc_cid', 'mc_eid', 'cmp', 'cmpid', 'at_medium', 'at_campaign', 'at_custom1', 'at_custom2', 'at_custom3', 'at_custom4', 'at_format', 'at_link_id', 'at_link_origin', 'at_link_type', 'at_bbc_team', 'source', 'xtor', 'ns_source', 'ns_mchannel', 'ns_campaign', 'ns_linkname', 'zalo_share', 'amp']);
export function chuanHoaLink(u: string): string {
  try {
    const x = new URL(u.trim());
    x.hash = '';
    for (const k of Array.from(x.searchParams.keys())) if (/^utm_/i.test(k) || THAM_SO_THEO_DOI.has(k.toLowerCase())) x.searchParams.delete(k);
    x.searchParams.sort();
    const host = x.hostname.toLowerCase().replace(/^www\./, '');
    const path = x.pathname.replace(/\/+$/, '') || '/';
    const q = x.searchParams.toString();
    return `${host}${path}${q ? '?' + q : ''}`;
  } catch (_) { return u.trim().toLowerCase(); }
}
// Link "sạch" để đưa cho người đọc: bỏ tham số theo dõi và #, giữ nguyên phần còn lại.
export function linkSach(u: string): string {
  try {
    const x = new URL(u.trim());
    x.hash = '';
    for (const k of Array.from(x.searchParams.keys())) if (/^utm_/i.test(k) || THAM_SO_THEO_DOI.has(k.toLowerCase())) x.searchParams.delete(k);
    return x.toString();
  } catch (_) { return u.trim(); }
}

export function tuCuaTieuDe(s: string): Set<string> {
  const bo = s.normalize('NFD').replace(/[̀-ͯ]/g, '').replace(/đ/g, 'd').replace(/Đ/g, 'd').toLowerCase();
  return new Set((bo.match(/[a-z0-9]+/g) || []).filter((w) => w.length >= 2));
}
// Độ giống = |giao| / |hợp| theo tập từ. Tiêu đề quá ngắn (< 4 từ) không so khớp mờ (tránh gộp nhầm).
export function doGiong(a: Set<string>, b: Set<string>): number {
  if (a.size < 4 || b.size < 4) return 0;
  let giao = 0;
  for (const w of a) if (b.has(w)) giao++;
  return giao / (a.size + b.size - giao);
}

// ---------- Gộp trùng ----------
// Giữ bản gặp đầu tiên (theo thứ tự nguồn trong nguon.ts), bản sau ghi tên báo vào `trung_voi` của bản giữ.
export function gopTrung(ds: Tin[], nguong = NGUONG_TRUNG_TIEU_DE): { tin: Tin[]; trung: number } {
  const giu: { t: Tin; link: string; tu: Set<string> }[] = [];
  let trung = 0;
  for (const t of ds) {
    const link = chuanHoaLink(t.link), tu = tuCuaTieuDe(t.tieu_de);
    const khop = giu.find((g) => g.link === link || doGiong(g.tu, tu) >= nguong);
    if (khop) {
      trung++;
      if (khop.t.bao !== t.bao) {
        khop.t.trung_voi = khop.t.trung_voi || [];
        if (!khop.t.trung_voi.includes(t.bao)) khop.t.trung_voi.push(t.bao);
      }
    } else giu.push({ t: { ...t }, link, tu });
  }
  return { tin: giu.map((g) => g.t), trung };
}

// ---------- Chuẩn hoá + lọc giờ + chọn chủ đề cho 1 nguồn ----------
export function chuanHoaNguon(tho: TinTho[], nguon: Nguon, bay_gio: number, gio = GIO_TOI_DA, toiDa = TOI_DA_MOI_NGUON): Tin[] {
  const tu = bay_gio - gio * 3600000, den = bay_gio + 2 * 3600000; // cho lệch đồng hồ 2 giờ
  const moi = tho
    .filter((x) => x.t !== null && x.t >= tu && x.t <= den) // tin không có giờ: bỏ (không biết có mới không)
    .sort((a, b) => (b.t as number) - (a.t as number))
    .map((x) => {
      const laTmdt = !!nguon.tmdt && TMDT_TU_KHOA.test(`${x.tieu_de} ${x.mo_ta}`);
      const ma: MaChuDe = laTmdt ? 'tmdt' : nguon.chu_de;
      return {
        chu_de: CHU_DE[ma], bao: nguon.bao, tieu_de: x.tieu_de, link: linkSach(x.link),
        mo_ta: catNgan(x.mo_ta, 300), thoi_gian: new Date(x.t as number).toISOString(),
      };
    });
  // Giới hạn tách riêng cho tin TMĐT (lọc từ khoá xong mới cắt) để không bị 15 tin mới nhất của mục kinh tế "ăn mất"
  const tm = moi.filter((x) => x.chu_de === CHU_DE.tmdt && nguon.chu_de !== 'tmdt');
  return [...moi.filter((x) => !tm.includes(x)).slice(0, toiDa), ...tm.slice(0, toiDa)];
}

// ---------- Hạn chót cho mỗi nguồn ----------
export function voiHanChot<T>(p: Promise<T>, ms: number, nhan = 'Quá thời gian'): Promise<T> {
  let h: ReturnType<typeof setTimeout>;
  const dong = new Promise<never>((_, rej) => { h = setTimeout(() => rej(new Error(`${nhan} (${ms} ms)`)), ms); });
  return Promise.race([p, dong]).finally(() => clearTimeout(h));
}

export type KetQua = {
  tin: Record<string, Tin[]>;
  loi: string[]; // "Báo (chủ đề)" của mọi nguồn lỗi, không trùng
  loi_chi_tiet: { bao: string; chu_de: string; url: string; ly_do: string }[];
  dem: { tong: number; truoc_khi_gop: number; da_gop_trung: number; theo_chu_de: Record<string, number>; theo_bao: Record<string, number>; nguon_ok: number; nguon_loi: number };
};

// Tải song song mọi nguồn. Nguồn nào lỗi/timeout/XML hỏng -> bỏ qua và ghi vào `loi`. Không bao giờ ném lỗi vì một nguồn.
export async function layTatCa(
  ds: Nguon[], tai: (url: string) => Promise<string>, bay_gio: number, han_chot = HAN_CHOT_MS,
): Promise<KetQua> {
  const kq = await Promise.all(ds.map(async (n) => {
    try {
      const xml = await voiHanChot(Promise.resolve().then(() => tai(n.url)), han_chot);
      return { n, tin: chuanHoaNguon(docRss(xml), n, bay_gio), loi: null as string | null };
    } catch (e) {
      return { n, tin: [] as Tin[], loi: e instanceof Error ? e.message : String(e) };
    }
  }));
  const loi: string[] = [], loi_chi_tiet: KetQua['loi_chi_tiet'] = [];
  const tatCa: Tin[] = [];
  for (const k of kq) {
    if (k.loi !== null) {
      const ten = `${k.n.bao} (${CHU_DE[k.n.chu_de]})`;
      if (!loi.includes(ten)) loi.push(ten);
      loi_chi_tiet.push({ bao: k.n.bao, chu_de: CHU_DE[k.n.chu_de], url: k.n.url, ly_do: k.loi });
    } else tatCa.push(...k.tin);
  }
  const { tin: duyet, trung } = gopTrung(tatCa);
  const tin: Record<string, Tin[]> = {};
  for (const ten of Object.values(CHU_DE)) tin[ten] = []; // chủ đề rỗng vẫn trả mảng rỗng
  for (const t of duyet) tin[t.chu_de].push(t);
  const theo_bao: Record<string, number> = {};
  for (const t of duyet) theo_bao[t.bao] = (theo_bao[t.bao] || 0) + 1;
  const theo_chu_de: Record<string, number> = {};
  for (const ten of Object.keys(tin)) {
    tin[ten].sort((a, b) => b.thoi_gian.localeCompare(a.thoi_gian));
    theo_chu_de[ten] = tin[ten].length;
  }
  return {
    tin, loi, loi_chi_tiet,
    dem: { tong: duyet.length, truoc_khi_gop: tatCa.length, da_gop_trung: trung, theo_chu_de, theo_bao, nguon_ok: kq.length - loi_chi_tiet.length, nguon_loi: loi_chi_tiet.length },
  };
}

// Edge Function "ban-tin-lay" (giai đoạn 2.8): tải RSS các báo đã chốt (nguon.ts) -> danh sách tin THÔ theo 7 chủ đề.
// Chưa dịch/tóm tắt/gửi Telegram (đó là 2.9). Không dùng khoá nào bên ngoài (RSS công khai).
// Quyền gọi: (a) chủ app đã đăng nhập (token + public.la_chu_app(), như "Gửi thử" của nhac-viec), hoặc (b) header x-cron-key = secret CRON_KEY.
// Deploy: tắt "Verify JWT" (function tự kiểm quyền). SUPABASE_URL / SUPABASE_ANON_KEY có sẵn tự động.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2';

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Headers': 'authorization, x-client-info, apikey, content-type, x-cron-key',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
};
const json = (o: unknown, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json', ...CORS } });

async function taiMotNguon(url: string): Promise<string> {
  // thử tối đa 2 lần (vài báo đôi khi cắt kết nối giữa chừng); mỗi lần có hạn chót riêng, tổng vẫn bị layTatCa chặn ở HAN_CHOT_MS
  let loi: unknown;
  for (let i = 0; i < 2; i++) {
    try {
      const r = await fetch(url, {
        signal: AbortSignal.timeout(HAN_CHOT_MS),
        headers: { 'User-Agent': 'Mozilla/5.0 (compatible; HarryAI-BanTin/1.0)', Accept: 'application/rss+xml, application/xml, text/xml, */*' },
      });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      return await r.text();
    } catch (e) { loi = e; }
  }
  throw loi;
}

Deno.serve(async (req) => {
  if (req.method === 'OPTIONS') return new Response('ok', { headers: CORS });
  const cron = req.headers.get('x-cron-key');
  if (cron) {
    const khoa = Deno.env.get('CRON_KEY');
    if (!khoa || cron !== khoa) return new Response('forbidden', { status: 403 });
  } else {
    const auth = req.headers.get('authorization') || '';
    if (!auth.startsWith('Bearer ')) return json({ loi: 'Cần đăng nhập' }, 401);
    const nguoi = createClient(Deno.env.get('SUPABASE_URL')!, Deno.env.get('SUPABASE_ANON_KEY')!, { global: { headers: { Authorization: auth } } });
    const { data: chu, error } = await nguoi.rpc('la_chu_app');
    if (error || chu !== true) return json({ loi: 'Chỉ chủ app được lấy tin' }, 403);
  }
  try {
    const kq = await layTatCa(NGUON, taiMotNguon, Date.now());
    return json(kq);
  } catch (e) {
    return json({ loi: 'Không lấy được tin: ' + (e instanceof Error ? e.message : String(e)) }, 500);
  }
});
