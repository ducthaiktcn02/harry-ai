// Bộ kiểm "ban-tin-gui" (2.9): phần thuần (loi.ts) + CHÍNH mã index.ts với Supabase giả, Gemini giả, Telegram giả, ban-tin-lay giả.
// Không mở mạng thật (chạy không có --allow-net). Chạy qua: py -3.12 tools/thu_ban_tin_gui_gia.py (cần deno). In ra JSON [{ten,dat,chi_tiet}].
import {
  cacLan, chonDuPhong, chonUngVien, dungNoiDung, dungPhanDau, dungPrompt, dungVanBanTelegram, escHtml, ghepTin, goiGemini, lamSachDauRa, ngayDep, ngayVN,
  CHU_DE_THU_TU,
} from '../supabase/functions/ban-tin-gui/loi.ts';
import type { KetQuaGemini, SuKienRow, Tin, YTuongRow } from '../supabase/functions/ban-tin-gui/loi.ts';

const kq: { ten: string; dat: boolean; chi_tiet: string }[] = [];
const kiem = (ten: string, dk: unknown, ct = '') => kq.push({ ten, dat: !!dk, chi_tiet: String(ct) });
const NOW = Date.parse('2026-11-26T01:00:00Z'); // 8:00 sáng thứ năm 26/11/2026 giờ VN
const [TD, TG, KT, CN, TM, SK, TT] = CHU_DE_THU_TU;

// ---------- dữ liệu mẫu ----------
let dem = 0;
const t = (chu_de: string, bao: string, tieu_de: string, mo_ta = 'Mô tả ngắn của bài.', link?: string): Tin =>
  ({ chu_de, bao, tieu_de, mo_ta, link: link ?? `https://${bao.toLowerCase().replace(/\s/g, '')}.example/bai-${++dem}`, thoi_gian: '2026-11-26T00:00:00.000Z' });
function mau(): Record<string, Tin[]> {
  dem = 0;
  const o: Record<string, Tin[]> = {};
  for (const c of CHU_DE_THU_TU) o[c] = [];
  for (let i = 1; i <= 10; i++) o[TD].push(t(TD, 'VnExpress', `Tin thời sự số ${i} về chính sách mới`, 'Chính phủ vừa ban hành quy định mới có hiệu lực từ đầu năm sau. '.repeat(i === 1 ? 12 : 1)));
  for (let i = 1; i <= 4; i++) o[TG].push(t(TG, 'BBC', `World leaders meet over climate fund ${i}`, 'Leaders agreed to raise contributions to the climate adaptation fund.'));
  for (let i = 1; i <= 3; i++) o[TG].push(t(TG, 'Tuổi Trẻ', `Tin thế giới số ${i} về hội nghị`, 'Hội nghị kết thúc với thoả thuận mới.'));
  for (let i = 1; i <= 9; i++) o[KT].push(t(KT, i % 2 ? 'Thanh Niên' : 'The Guardian', i % 2 ? `Giá vàng trong nước phiên số ${i}` : `Markets rally as inflation cools ${i}`, 'Vàng miếng biến động nhẹ theo giá thế giới.'));
  for (let i = 1; i <= 5; i++) o[CN].push(t(CN, 'VOV', `Công nghệ AI mới số ${i} ra mắt`, 'Mô hình chạy trực tiếp trên máy.'));
  o[TM].push(t(TM, 'Tuổi Trẻ', 'Sàn TMĐT siết quy định hàng giả', 'Người bán phải bổ sung giấy tờ nguồn gốc.'));
  o[SK].push(t(SK, 'Báo Chính phủ', 'Bộ Y tế khuyến cáo phòng cúm mùa'), t(SK, 'BBC', 'Sleep and heart risk study published', 'A study of 90,000 people.'), t(SK, 'The Guardian', 'NHS waiting lists fall slightly', ''));
  o[TT].push(t(TT, 'BBC', 'Premier League leaders win 2-0', 'The result extends the lead to four points.'), t(TT, 'The Guardian', 'Cricket: tourists chase 300', 'Tourists need 300 to win.'));
  // tin độc hại để kiểm escape / loại link lạ
  o[TD].push(t(TD, 'Báo Lạ', '<img src=x onerror=alert(1)> Tin có thẻ HTML & ký tự đặc biệt "ngoặc"', 'Mô tả <script>alert(1)</script> tồi', 'javascript:alert(1)'));
  return o;
}
const dsTat = (o: Record<string, Tin[]>) => Object.values(o).flat();

// ================= 1) chọn ứng viên =================
const tin0 = mau();
const uv = chonUngVien(tin0);
kiem('Ứng viên: tối đa 8 tin/chủ đề', CHU_DE_THU_TU.every((c) => uv.filter((u) => u.chu_de === c).length <= 8), CHU_DE_THU_TU.map((c) => uv.filter((u) => u.chu_de === c).length).join(','));
kiem('Ứng viên: id số liên tục 1..n, không trùng link', uv.every((u, i) => u.id === i + 1) && new Set(uv.map((u) => u.link)).size === uv.length);
kiem('Ứng viên: bỏ tin có link không phải http(s) (javascript:)', !uv.some((u) => u.link.startsWith('javascript')));
kiem('Ứng viên: mô tả cắt ≤ 240 ký tự (tiết kiệm token)', uv.every((u) => Array.from(u.mo_ta).length <= 240) && Array.from(tin0[TD][0].mo_ta).length > 240);
kiem('Ứng viên: nhận ngôn ngữ vi/en theo dấu tiếng Việt', uv.find((u) => u.bao === 'BBC')?.ngon_ngu === 'en' && uv.find((u) => u.bao === 'VOV')?.ngon_ngu === 'vi');
kiem('Ứng viên: đủ 7 chủ đề khi có tin', new Set(uv.map((u) => u.chu_de)).size === 7);

// ================= 2) prompt =================
const p = dungPrompt(uv);
const dl = JSON.parse(p.noi_dung);
kiem('Prompt: dữ liệu là JSON, mỗi tin có id/chu_de/bao/tieu_de/mo_ta', Array.isArray(dl) && dl.length === uv.length && dl.every((x: any) => typeof x.id === 'number' && x.tieu_de && x.chu_de && x.bao));
kiem('Prompt: KHÔNG gửi link cho Gemini (link luôn lấy từ dữ liệu gốc)', !p.noi_dung.includes('http'));
kiem('Prompt: có quy tắc cấm bịa + coi nội dung là dữ liệu + bù TMĐT bằng Kinh tế', /TUYỆT ĐỐI không thêm/.test(p.he_thong) && /DỮ LIỆU/.test(p.he_thong) && p.he_thong.includes('Kinh doanh online / TMĐT') && p.he_thong.includes('Kinh tế – tài chính'));

// ================= 3) lọc đầu ra =================
const idDau = uv[0].id, idEn = uv.find((u) => u.ngon_ngu === 'en')!.id;
const raw = { tin: [
  { id: idDau, tieu_de_vi: 'Tiêu đề đã dịch', tom_tat: 'Tóm tắt 2 câu.', link: 'https://gian-lan.example', bao: 'Báo bịa' },
  { id: idDau, tieu_de_vi: 'Trùng id', tom_tat: 'x' },
  { id: 9999, tieu_de_vi: 'Chỉ số bịa', tom_tat: 'x' },
  { id: -1, tieu_de_vi: 'Âm', tom_tat: 'x' },
  { id: 1.5, tieu_de_vi: 'Số lẻ', tom_tat: 'x' },
  { id: '3', tieu_de_vi: 'Chuỗi', tom_tat: 'x' },
  null, 'abc',
  { id: idEn, tieu_de_vi: '', tom_tat: 'T'.repeat(2000) },
] };
const ls = lamSachDauRa(raw, uv);
kiem('Lọc đầu ra: bỏ id lạ/trùng/âm/lẻ/chuỗi/rác, chỉ còn 2 mục hợp lệ', ls.muc.length === 2 && ls.bo === 7, `${ls.muc.length} mục, bỏ ${ls.bo}`);
kiem('Lọc đầu ra: link + tên báo luôn lấy từ dữ liệu gốc, không từ Gemini', ls.muc[0].link === uv[0].link && ls.muc[0].bao === uv[0].bao && !JSON.stringify(ls.muc).includes('gian-lan'));
kiem('Lọc đầu ra: thiếu tiêu đề dịch thì dùng tiêu đề gốc; tóm tắt cắt ≤ 600', ls.muc[1].tieu_de === uv.find((u) => u.id === idEn)!.tieu_de.slice(0, 160) && Array.from(ls.muc[1].tom_tat).length <= 600 && ls.muc[1].ai === false);
kiem('Lọc đầu ra: đầu ra không phải đối tượng -> 0 mục', lamSachDauRa(null, uv).muc.length === 0 && lamSachDauRa({ tin: 'x' }, uv).muc.length === 0 && lamSachDauRa(42, uv).muc.length === 0);
kiem('Lọc đầu ra: tối đa 15 mục', lamSachDauRa({ tin: uv.map((u) => ({ id: u.id, tieu_de_vi: 'a b c', tom_tat: 'd e f' })) }, uv).muc.length === 15);

// ================= 4) dự phòng không AI =================
const dp = chonDuPhong(uv);
kiem('Dự phòng: đúng 12 tin, không trùng link', dp.length === 12 && new Set(dp.map((m) => m.link)).size === 12, String(dp.length));
kiem('Dự phòng: mọi chủ đề có tin đều xuất hiện', CHU_DE_THU_TU.every((c) => dp.some((m) => m.chu_de === c)), CHU_DE_THU_TU.map((c) => dp.filter((m) => m.chu_de === c).length).join(','));
kiem('Dự phòng: TMĐT chỉ có 1 tin -> phần còn thiếu bù bằng Kinh tế (Kinh tế ≥ 3 tin)', dp.filter((m) => m.chu_de === TM).length === 1 && dp.filter((m) => m.chu_de === KT).length >= 3, `KT=${dp.filter((m) => m.chu_de === KT).length}`);
const en0 = dp.find((m) => m.ngon_ngu === 'en')!;
kiem('Dự phòng: tin tiếng Anh giữ nguyên tiêu đề + mô tả gốc, đánh dấu ngon_ngu=en, ai=false', en0 && en0.ai === false && uv.some((u) => u.tieu_de === en0.tieu_de && u.link === en0.link) && (en0.tom_tat === '' || uv.some((u) => u.mo_ta === en0.tom_tat)));
kiem('Dự phòng: ít tin hơn 12 thì lấy hết (không lỗi)', chonDuPhong(uv.slice(0, 4)).length === 4 && chonDuPhong([]).length === 0);

// ================= 5) ghép Gemini + dự phòng =================
const gemOk = (n: number): KetQuaGemini => ({ ok: true, so_lan: 1, bo: 0, muc: ls.muc.length ? uv.slice(0, n).map((u) => ({ chu_de: u.chu_de, bao: u.bao, link: u.link, tieu_de: 'VI ' + u.tieu_de, tom_tat: 'ts', ngon_ngu: 'vi' as const, ai: true })) : [] });
const g6 = ghepTin(uv, gemOk(6));
kiem('Ghép: Gemini chỉ trả 6 tin -> bù dự phòng cho đủ 10, không trùng', g6.tin.length === 10 && new Set(g6.tin.map((m) => m.link)).size === 10 && g6.dung_ai && g6.tin.filter((m) => m.ai).length === 6);
const gLoi = ghepTin(uv, { ok: false, loai: 'het_luot', ly_do: 'Gemini hết lượt miễn phí (429)', so_lan: 1 });
kiem('Ghép: Gemini lỗi -> dự phòng 12 tin, dung_ai=false, có lý do', gLoi.tin.length === 12 && !gLoi.dung_ai && /429/.test(gLoi.ly_do || ''));
kiem('Ghép: tin xếp theo thứ tự chủ đề', gLoi.tin.every((m, i, a) => i === 0 || CHU_DE_THU_TU.indexOf(a[i - 1].chu_de) <= CHU_DE_THU_TU.indexOf(m.chu_de)));

// ================= 6) goiGemini với fetch giả =================
function gemFetch(mode: string[]) {
  const goi: { khoa: string | null; body: any }[] = [];
  const f = (async (_u: string, init: any) => {
    const body = JSON.parse(init.body); goi.push({ khoa: init.headers['x-goog-api-key'], body });
    const m = mode[Math.min(goi.length - 1, mode.length - 1)];
    if (m === 'net') throw new Error('mạng chết');
    if (m === '429') return new Response('{}', { status: 429 });
    if (m === '404') return new Response('{}', { status: 404 });
    if (m === '403') return new Response('{}', { status: 403 });
    if (m === '500') return new Response('{}', { status: 500 });
    const wrap = (s: string) => new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: s }] } }] }), { status: 200 });
    if (m === 'junk') return wrap('không phải json {{');
    if (m === 'rong') return new Response(JSON.stringify({ candidates: [] }), { status: 200 });
    const ds = JSON.parse(body.contents[0].parts[0].text) as any[];
    if (m === 'bia') return wrap(JSON.stringify({ tin: ds.map((_, i) => ({ id: 1000 + i, tieu_de_vi: 'Bịa', tom_tat: 'Bịa' })) }));
    // ok: mỗi chủ đề lấy 2 tin đầu
    const chon: any[] = []; const dem: Record<string, number> = {};
    for (const x of ds) { dem[x.chu_de] = (dem[x.chu_de] || 0) + 1; if (dem[x.chu_de] <= 2) chon.push({ id: x.id, tieu_de_vi: 'VI: ' + x.tieu_de, tom_tat: 'Tóm tắt: ' + x.mo_ta }); }
    return wrap(JSON.stringify({ tin: chon }));
  }) as unknown as typeof fetch;
  return { f, goi };
}
{
  const a = gemFetch(['ok']); const r = await goiGemini(uv, 'KHOA-GIA', a.f);
  kiem('Gemini giả OK: 1 lần gọi, đúng khoá + schema + model nhẹ + JSON', r.ok && a.goi.length === 1 && a.goi[0].khoa === 'KHOA-GIA' && a.goi[0].body.generationConfig.responseMimeType === 'application/json' && !!a.goi[0].body.generationConfig.responseSchema, JSON.stringify(r).slice(0, 120));
  const b = gemFetch(['429', 'ok']); const r2 = await goiGemini(uv, 'K', b.f);
  kiem('Gemini 429 (hết lượt): KHÔNG gọi lại (đúng 1 lần), trả lý do hết lượt', !r2.ok && r2.loai === 'het_luot' && b.goi.length === 1);
  const c = gemFetch(['500', 'ok']); const r3 = await goiGemini(uv, 'K', c.f);
  kiem('Gemini 500 rồi OK: thử lại 1 lần (tối đa 2 lần/ngày)', r3.ok && c.goi.length === 2 && r3.so_lan === 2);
  const d = gemFetch(['junk', 'junk', 'ok']); const r4 = await goiGemini(uv, 'K', d.f);
  kiem('Gemini JSON hỏng 2 lần: dừng ở 2 lần gọi, báo lỗi (không gọi lần 3)', !r4.ok && r4.loai === 'dau_ra_xau' && d.goi.length === 2);
  const e = gemFetch(['bia']); const r5 = await goiGemini(uv, 'K', e.f);
  kiem('Gemini bịa chỉ số: mọi mục bị bỏ -> coi là hỏng (chuyển dự phòng)', !r5.ok && r5.loai === 'dau_ra_xau');
  const f1 = gemFetch(['net']); const r6 = await goiGemini(uv, 'K', f1.f);
  kiem('Mạng chết: báo lỗi tạm thời, thử 2 lần, không ném lỗi', !r6.ok && r6.loai === 'tam_thoi' && f1.goi.length === 2);
  const g = gemFetch(['404']); const r7 = await goiGemini(uv, 'K', g.f);
  kiem('Gemini 404 (model bị gỡ) có lý do riêng, 1 lần gọi', !r7.ok && r7.loai === 'khong_co_model' && g.goi.length === 1);
  const h = gemFetch(['403']); const r8 = await goiGemini(uv, 'K', h.f);
  kiem('Gemini 403 (khoá sai): lý do riêng, không gọi lại', !r8.ok && r8.loai === 'khoa_sai' && h.goi.length === 1);
  const i = gemFetch(['ok']); const r9 = await goiGemini(uv, undefined, i.f);
  kiem('Không có khoá: không gọi mạng', !r9.ok && r9.loai === 'khong_co_khoa' && i.goi.length === 0);
  const j = gemFetch(['rong']); const r10 = await goiGemini(uv, 'K', j.f);
  kiem('Gemini trả rỗng (candidates=[]): lỗi đầu ra, không ném', !r10.ok);
}

// ================= 7) phần đầu =================
const ev = (tieu_de: string, bd: string, kt: string, o: Partial<SuKienRow> = {}): SuKienRow => ({ tieu_de, bat_dau: bd, ket_thuc: kt, ca_ngay: false, lap: 'none', lap_den: null, lap_ngoai: [], ...o });
const SKS: SuKienRow[] = [
  ev('A. Họp sáng', '2026-11-26T02:00:00Z', '2026-11-26T03:00:00Z'),
  ev('B. Hôm qua', '2026-11-25T02:00:00Z', '2026-11-25T03:00:00Z'),
  ev('C. Lặp ngày', '2026-11-20T07:00:00Z', '2026-11-20T08:00:00Z', { lap: 'day' }),
  ev('D. Lặp ngày bỏ hôm nay', '2026-11-20T08:00:00Z', '2026-11-20T09:00:00Z', { lap: 'day', lap_ngoai: ['2026-11-26T08:00:00.000Z'] }),
  ev('E. Lặp ngày đã hết hạn', '2026-11-20T09:00:00Z', '2026-11-20T10:00:00Z', { lap: 'day', lap_den: '2026-11-25' }),
  ev('F. Lặp tuần (thứ năm)', '2026-11-19T13:00:00Z', '2026-11-19T14:00:00Z', { lap: 'week' }),
  ev('G. Lặp tuần (thứ tư)', '2026-11-18T13:00:00Z', '2026-11-18T14:00:00Z', { lap: 'week' }),
  ev('H. Lặp tháng (26)', '2026-10-26T01:30:00Z', '2026-10-26T02:30:00Z', { lap: 'month' }),
  ev('I. Cả ngày hôm nay', '2026-11-25T17:00:00Z', '2026-11-26T17:00:00Z', { ca_ngay: true }),
  ev('J. Cả ngày mai', '2026-11-26T17:00:00Z', '2026-11-27T17:00:00Z', { ca_ngay: true }),
  ev('K. Kéo qua nửa đêm', '2026-11-25T16:00:00Z', '2026-11-25T19:00:00Z'),
  ev('L. Tối nay 23:30', '2026-11-26T16:30:00Z', '2026-11-26T17:30:00Z'),
];
const y = (tieu_de: string, o: Partial<YTuongRow> & { tuoi?: number } = {}): YTuongRow => ({ tieu_de, trang_thai: 'chua_lam', han: null, sua_luc: new Date(NOW - (o.tuoi ?? 1) * 86400000).toISOString(), xoa_luc: null, ...o });
const YTS: YTuongRow[] = [
  y('Trễ 1', { han: '2026-11-20' }), y('Trễ 2 đang làm', { han: '2026-11-25', trang_thai: 'dang_lam' }), y('Hạn hôm nay', { han: '2026-11-26' }),
  y('Hạn mai', { han: '2026-11-27' }), y('Trễ nhưng đã xong', { han: '2026-11-01', trang_thai: 'xong' }), y('Trễ nhưng đã xoá', { han: '2026-11-01', xoa_luc: '2026-11-20T00:00:00Z' }),
  y('Lâu 40', { tuoi: 40 }), y('Lâu 30', { tuoi: 30 }), y('Lâu 20', { tuoi: 20 }), y('Lâu 15', { tuoi: 15 }), y('Mới 14', { tuoi: 14 }),
  y('Lâu nhưng đang làm', { tuoi: 90, trang_thai: 'dang_lam' }), y('Lâu nhưng đã xong', { tuoi: 90, trang_thai: 'xong' }), y('Lâu nhưng đã xoá', { tuoi: 90, xoa_luc: '2026-11-20T00:00:00Z' }),
  y('Lâu nhưng đã trễ hạn', { tuoi: 100, han: '2026-11-10' }),
];
const dau = dungPhanDau(SKS, YTS, NOW);
const ten = dau.lich.map((e) => e.tieu_de.slice(0, 1));
kiem('Lịch hôm nay: đúng các sự kiện (A,C,F,H,I,K,L) kể cả lặp ngày/tuần/tháng + cả ngày + kéo qua nửa đêm', ten.sort().join('') === 'ACFHIKL', ten.join(''));
kiem('Lịch hôm nay: bỏ hôm qua, ngoại lệ lặp (D), lặp hết hạn (E), lặp tuần khác thứ (G), cả ngày mai (J)', !['B', 'D', 'E', 'G', 'J'].some((c) => ten.includes(c)));
const lichTheoGio = dungPhanDau(SKS, YTS, NOW).lich;
kiem('Lịch hôm nay: cả ngày đứng đầu, sau đó theo giờ tăng dần', lichTheoGio[0].ca_ngay && lichTheoGio.slice(1).every((e, i, a) => i === 0 || (a[i - 1].gio as string) <= (e.gio as string)), lichTheoGio.map((e) => e.gio ?? 'CN').join(' '));
kiem('Lịch hôm nay: giờ hiển thị theo giờ VN (A = 09:00–10:00, L = 23:30–00:30 không ghi giờ kết)', lichTheoGio.find((e) => e.tieu_de.startsWith('A'))?.gio === '09:00' && lichTheoGio.find((e) => e.tieu_de.startsWith('A'))?.gio_ket === '10:00' && lichTheoGio.find((e) => e.tieu_de.startsWith('L'))?.gio === '23:30' && lichTheoGio.find((e) => e.tieu_de.startsWith('L'))?.gio_ket === null, JSON.stringify(lichTheoGio.find((e) => e.tieu_de.startsWith('L'))));
kiem('Việc trễ hạn: chỉ ý tưởng có hạn < hôm nay, chưa xong, chưa xoá, hạn cũ trước', dau.tre_han.map((x) => x.tieu_de).join('|') === 'Lâu nhưng đã trễ hạn|Trễ 1|Trễ 2 đang làm', dau.tre_han.map((x) => x.tieu_de).join('|'));
kiem('Ý tưởng để lâu: tối đa 3, chỉ "chưa làm" >14 ngày, cũ nhất trước, bỏ đã xoá/đang làm/xong/đã trễ hạn (không lặp)', dau.de_lau.map((x) => x.tieu_de).join('|') === 'Lâu 40|Lâu 30|Lâu 20' && dau.de_lau[0].so_ngay === 40, dau.de_lau.map((x) => x.tieu_de + x.so_ngay).join('|'));
kiem('Phần đầu rỗng khi không có dữ liệu', (() => { const d = dungPhanDau([], [], NOW); return !d.lich.length && !d.tre_han.length && !d.de_lau.length; })());
kiem('Bung lặp tháng 31: tháng không có ngày 31 thì bỏ', cacLan(ev('x', '2026-10-31T02:00:00Z', '2026-10-31T03:00:00Z', { lap: 'month' }), Date.parse('2026-11-01T00:00:00Z'), Date.parse('2026-12-31T23:00:00Z')).length === 1);

// ================= 8) văn bản Telegram =================
const ndFull = dungNoiDung('2026-11-26', NOW, dau, uv, { ok: true, so_lan: 1, bo: 0, muc: ls.muc }, ['Báo Lỗi (Thế giới)']);
const xss = uv.length ? { ...uv[0], tieu_de: '<b>Chèn</b> & "x" <script>', mo_ta: '</a><a href="javascript:alert(1)">bấm' } : uv[0];
const ndXss = dungNoiDung('2026-11-26', NOW, dau, [xss], null, []);
ndXss.tin = [{ chu_de: TD, bao: 'Báo <i>lạ</i>', tieu_de: '<img src=x onerror=1> & "q"', tom_tat: '</b><a href="javascript:alert(1)">x</a>', link: 'https://a.example/x?a=1&b=2"onmouseover="x', ngon_ngu: 'vi', ai: true }];
const vbXss = dungVanBanTelegram(ndXss).join('\n');
kiem('Telegram: escape HTML (không còn thẻ <img>, <script>, <i> thô của nội dung)', !/<img|<script|<i>lạ|<a href="javascript/i.test(vbXss) && vbXss.includes('&lt;img src=x onerror=1&gt; &amp; &quot;q&quot;'), vbXss.slice(0, 300));
kiem('Telegram: link trong href được escape (& -> &amp;, " -> &quot;)', vbXss.includes('href="https://a.example/x?a=1&amp;b=2&quot;onmouseover=&quot;x"'));
const nd15 = { ...ndFull, tin: Array.from({ length: 15 }, (_, i) => ({ chu_de: CHU_DE_THU_TU[i % 7], bao: 'Báo ' + i, tieu_de: 'Tiêu đề rất dài '.repeat(10) + i, tom_tat: 'Tóm tắt rất dài '.repeat(40), link: 'https://a.example/' + i, ngon_ngu: 'vi' as const, ai: true })) };
const khuc15 = dungVanBanTelegram(nd15);
kiem('Telegram: bản tin dài được chia khúc, mỗi khúc < 4096 ký tự', khuc15.length > 1 && khuc15.every((k) => k.length < 4096), khuc15.map((k) => k.length).join(','));
const ndBat = { ...ndFull, tin: [{ chu_de: TD, bao: 'B', tieu_de: '&'.repeat(160), tom_tat: '&'.repeat(600), link: 'https://a.example/' + 'x&'.repeat(240), ngon_ngu: 'vi' as const, ai: true }, ...ndFull.tin], loi_nguon: [] };
kiem('Telegram: trường hợp xấu nhất (toàn ký tự cần escape) vẫn mọi khúc < 4096', dungVanBanTelegram(ndBat).every((k) => k.length < 4096), dungVanBanTelegram(ndBat).map((k) => k.length).join(','));
const vbOk = dungVanBanTelegram(ndFull).join('\n');
kiem('Telegram: có tiêu đề ngày, lịch hôm nay, trễ hạn, để lâu, tên báo + link, dòng "không lấy được tin từ"', vbOk.includes('Bản tin sáng — Thứ năm, 26/11/2026') && vbOk.includes('Lịch hôm nay') && vbOk.includes('Việc trễ hạn') && vbOk.includes('Ý tưởng để lâu') && vbOk.includes('<a href="https://') && vbOk.includes('Hôm nay không lấy được tin từ: Báo Lỗi (Thế giới)'));
const vbDp = dungVanBanTelegram(dungNoiDung('2026-11-26', NOW, dau, uv, { ok: false, loai: 'het_luot', ly_do: 'Gemini hết lượt miễn phí (429)', so_lan: 1 }, [])).join('\n');
kiem('Telegram: khi không có AI có cảnh báo + đánh dấu (tiếng Anh) ở tin nước ngoài', vbDp.includes('chưa dịch/tóm tắt được') && vbDp.includes('(tiếng Anh)'));
kiem('ngayDep / escHtml cơ bản', ngayDep('2026-11-29') === 'Chủ nhật, 29/11/2026' && escHtml('<&>"') === '&lt;&amp;&gt;&quot;');

// ================= 9) CHÍNH index.ts với mọi thứ giả =================
const G: any = globalThis;
let handler: (r: Request) => Promise<Response> = async () => new Response('chưa nạp');
(Deno as any).serve = (h: any) => { handler = h; };
Deno.env.set('SUPABASE_URL', 'https://gia.supabase.co'); Deno.env.set('SUPABASE_ANON_KEY', 'anon-gia'); Deno.env.set('SUPABASE_SERVICE_ROLE_KEY', 'service-gia');
Deno.env.set('CRON_KEY', 'MA-CRON-GIA'); Deno.env.set('GEMINI_API_KEY', 'KHOA-GEMINI-GIA'); Deno.env.set('TELEGRAM_BOT_TOKEN', 'BOT-GIA'); Deno.env.set('TELEGRAM_CHAT_ID', '123');
await import('../supabase/functions/ban-tin-gui/index.ts');

type Cau = { gem?: string[]; tg?: string; lay?: string; sk?: any[]; yt?: any[]; khongKhoaGemini?: boolean; laChu?: boolean };
function datLai(c: Cau = {}) {
  G.__FAKE = {
    db: { ban_tin: [], su_kien: c.sk ?? SK_DB(), y_tuong: c.yt ?? YT_DB() }, laChu: c.laChu ?? true, nhatKy: [], loiBang: {},
    gem: [] as any[], tg: [] as string[], lay: 0, gemMode: c.gem ?? ['ok'], tgMode: c.tg ?? 'ok', layMode: c.lay ?? 'ok',
  };
  if (c.khongKhoaGemini) Deno.env.delete('GEMINI_API_KEY'); else Deno.env.set('GEMINI_API_KEY', 'KHOA-GEMINI-GIA');
}
const homNayVN = () => ngayVN(Date.now());
// sự kiện/ý tưởng giả theo giờ thật của máy (hàm dựng phần đầu dùng Date.now())
function SK_DB() { const d = homNayVN(); return [{ tieu_de: 'Họp khách hôm nay', bat_dau: new Date(Date.parse(d + 'T00:00:00Z') - 7 * 3600000 + 9 * 3600000).toISOString(), ket_thuc: new Date(Date.parse(d + 'T00:00:00Z') - 7 * 3600000 + 10 * 3600000).toISOString(), ca_ngay: false, lap: 'none', lap_den: null, lap_ngoai: [], xoa_luc: null }]; }
function YT_DB() { const cu = (n: number) => new Date(Date.now() - n * 86400000).toISOString(); return [
  { tieu_de: 'Ý tưởng để lâu 30', trang_thai: 'chua_lam', han: null, sua_luc: cu(30), xoa_luc: null },
  { tieu_de: 'Việc trễ hạn', trang_thai: 'dang_lam', han: '2020-01-01', sua_luc: cu(1), xoa_luc: null }]; }
G.fetch = async (url: string, init: any) => {
  const F = G.__FAKE; const u = String(url);
  if (u.includes('/functions/v1/ban-tin-lay')) {
    F.lay++;
    if (init?.headers?.['x-cron-key'] !== 'MA-CRON-GIA') return new Response('forbidden', { status: 403 });
    if (F.layMode === 'net') throw new Error('mạng chết');
    if (F.layMode === '500') return new Response('{}', { status: 500 });
    if (F.layMode === '404') return new Response('{}', { status: 404 });
    return new Response(JSON.stringify({ tin: mau(), loi: ['Báo Hỏng (Thế giới)'], dem: {} }), { status: 200 });
  }
  if (u.includes('generativelanguage.googleapis.com')) {
    const body = JSON.parse(init.body); F.gem.push({ khoa: init.headers['x-goog-api-key'], u });
    const m = F.gemMode[Math.min(F.gem.length - 1, F.gemMode.length - 1)];
    if (m === '429') return new Response('{}', { status: 429 });
    if (m === 'junk') return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: '{{hỏng' }] } }] }), { status: 200 });
    const ds = JSON.parse(body.contents[0].parts[0].text) as any[];
    if (m === 'bia') return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify({ tin: [{ id: 777, tieu_de_vi: 'Bịa', tom_tat: 'Bịa' }] }) }] } }] }), { status: 200 });
    const chon: any[] = []; const dem: Record<string, number> = {};
    for (const x of ds) { dem[x.chu_de] = (dem[x.chu_de] || 0) + 1; if (dem[x.chu_de] <= 2) chon.push({ id: x.id, tieu_de_vi: m === 'xss' ? '<script>alert(1)</script> ' + x.tieu_de : 'VI: ' + x.tieu_de, tom_tat: m === 'xss' ? '</b><a href="javascript:alert(1)">bấm</a>' : 'Tóm tắt: ' + x.mo_ta }); }
    return new Response(JSON.stringify({ candidates: [{ content: { parts: [{ text: JSON.stringify({ tin: chon }) }] } }] }), { status: 200 });
  }
  if (u.includes('api.telegram.org')) {
    if (F.tgMode === 'net') throw new Error('mạng chết');
    if (F.tgMode === '400') return new Response('{"ok":false}', { status: 400 });
    F.tg.push(JSON.parse(init.body)); return new Response('{"ok":true}', { status: 200 });
  }
  throw new Error('Gọi mạng ngoài dự kiến: ' + u);
};
const goi = async (kieu: 'cron' | 'chu' | 'khong' | 'cron-sai', body: any = {}) => {
  const h: Record<string, string> = { 'Content-Type': 'application/json' };
  if (kieu === 'cron') h['x-cron-key'] = 'MA-CRON-GIA'; if (kieu === 'cron-sai') h['x-cron-key'] = 'sai'; if (kieu === 'chu') h['authorization'] = 'Bearer TOKEN-CHU';
  const res = await handler(new Request('https://gia/functions/v1/ban-tin-gui', { method: 'POST', headers: h, body: JSON.stringify(body) }));
  const text = await res.text(); let j: any = null; try { j = JSON.parse(text); } catch (_) { /* không phải JSON */ }
  return { s: res.status, j, text };
};
const F = () => G.__FAKE;
const hang = () => F().db.ban_tin[0];
const tgText = () => F().tg.map((x: any) => x.text).join('\n');

// --- quyền ---
datLai();
kiem('Quyền: không đăng nhập, không cron -> 401', (await goi('khong')).s === 401);
kiem('Quyền: sai x-cron-key -> 403, không tạo gì', (await goi('cron-sai')).s === 403 && F().db.ban_tin.length === 0 && F().gem.length === 0);
datLai({ laChu: false });
kiem('Quyền: tài khoản không phải chủ app -> 403, không gọi Gemini/Telegram', (await goi('chu')).s === 403 && F().gem.length === 0 && F().tg.length === 0);

// --- đường thường: cron 8:00 ---
datLai();
let r = await goi('cron');
kiem('Cron: tạo bản tin + gửi Telegram, 1 lần gọi Gemini, đúng khoá', r.s === 200 && r.j.tao_moi && r.j.da_gui && r.j.gui_lan_nay && F().gem.length === 1 && F().gem[0].khoa === 'KHOA-GEMINI-GIA' && F().tg.length >= 1, JSON.stringify(r.j));
kiem('Cron: bảng ban_tin có đúng 1 dòng ngày hôm nay (giờ VN), có telegram_luc', F().db.ban_tin.length === 1 && hang().ngay === homNayVN() && !!hang().telegram_luc);
const nd = hang().noi_dung;
kiem('Bản tin lưu: 10–15 tin, dung_ai, đủ 7 chủ đề, mỗi tin có báo + link http(s) lấy từ dữ liệu gốc', nd.tin.length >= 10 && nd.tin.length <= 15 && nd.dung_ai && new Set(nd.tin.map((m: any) => m.chu_de)).size === 7 && nd.tin.every((m: any) => m.bao && /^https?:\/\//.test(m.link)), `${nd.tin.length} tin`);
const linkGoc = new Set(dsTat(mau()).map((m) => m.link));
kiem('Bản tin lưu: mọi link đều nằm trong dữ liệu gốc (không có link Gemini tự bịa)', nd.tin.every((m: any) => linkGoc.has(m.link)));
kiem('Bản tin lưu: phần đầu có lịch hôm nay, việc trễ hạn, ý tưởng để lâu', nd.dau.lich.some((e: any) => e.tieu_de === 'Họp khách hôm nay' && e.gio === '09:00') && nd.dau.tre_han[0]?.tieu_de === 'Việc trễ hạn' && nd.dau.de_lau[0]?.tieu_de === 'Ý tưởng để lâu 30', JSON.stringify(nd.dau).slice(0, 200));
kiem('Bản tin lưu: ghi các báo lỗi lấy tin (loi_nguon)', nd.loi_nguon.includes('Báo Hỏng (Thế giới)'));
kiem('Telegram nhận: có nội dung đã dịch (VI:), parse_mode HTML, chat_id đúng, tắt xem trước link, mọi khúc < 4096', tgText().includes('VI: ') && F().tg.every((x: any) => x.parse_mode === 'HTML' && x.chat_id === '123' && x.disable_web_page_preview === true && x.text.length < 4096), F().tg.map((x: any) => x.text.length).join(','));
const gemLan1 = F().gem.length, tgLan1 = F().tg.length;
r = await goi('cron');
kiem('Chống trùng: cron chạy lại cùng ngày -> KHÔNG gọi Gemini, KHÔNG gửi Telegram nữa, vẫn báo đã gửi', r.s === 200 && !r.j.tao_moi && r.j.da_gui && !r.j.gui_lan_nay && F().gem.length === gemLan1 && F().tg.length === tgLan1 && F().db.ban_tin.length === 1, JSON.stringify(r.j));
r = await goi('chu', { ep: true });
kiem('Chủ app ép tạo lại (ep): tạo lại + gửi lại Telegram, vẫn 1 dòng/ngày', r.s === 200 && r.j.tao_moi && r.j.gui_lan_nay && F().gem.length === gemLan1 + 1 && F().tg.length > tgLan1 && F().db.ban_tin.length === 1);
kiem('Không lộ khoá / token trong kết quả trả về hay nội dung Telegram', ![r.text, tgText(), JSON.stringify(hang())].some((s) => /KHOA-GEMINI-GIA|BOT-GIA|MA-CRON-GIA|TOKEN-CHU|service-gia/.test(s)));

// --- nút trong app: chi_tao ---
datLai();
r = await goi('chu', { chi_tao: true });
kiem('Nút "Tạo bản tin hôm nay" (chi_tao): lưu bản tin, KHÔNG gửi Telegram', r.s === 200 && r.j.tao_moi && !r.j.da_gui && F().tg.length === 0 && hang().telegram_luc === null && F().db.ban_tin.length === 1, JSON.stringify(r.j));
const g1 = F().gem.length;
r = await goi('chu', { chi_tao: true });
kiem('Bấm nút lần 2 khi đã có bản tin (không ep): không tạo lại, không tốn lượt Gemini', r.s === 200 && !r.j.tao_moi && F().gem.length === g1);
r = await goi('cron');
kiem('Sau đó cron 8:00: dùng lại bản đã tạo (không gọi Gemini lại), gửi Telegram, đặt telegram_luc', r.s === 200 && !r.j.tao_moi && r.j.gui_lan_nay && F().gem.length === g1 && F().tg.length >= 1 && !!hang().telegram_luc);

// --- Gemini lỗi -> dự phòng tiếng Anh ---
for (const [ten, gem, soGoi] of [['429 hết lượt', ['429'], 1], ['JSON hỏng', ['junk'], 2], ['chỉ số bịa', ['bia'], 2]] as [string, string[], number][]) {
  datLai({ gem });
  r = await goi('cron');
  const n = hang()?.noi_dung;
  kiem(`Gemini ${ten}: vẫn ra bản tin 12 tin dự phòng (tiếng Anh nguyên gốc) + vẫn gửi Telegram (${soGoi} lần gọi Gemini)`, r.s === 200 && n && !n.dung_ai && n.tin.length === 12 && n.ly_do_khong_ai && F().gem.length === soGoi && r.j.da_gui && F().tg.length >= 1, `dung_ai=${n?.dung_ai} tin=${n?.tin.length} goi=${F().gem.length}`);
  if (ten === '429 hết lượt') {
    const goc = new Set(dsTat(mau()).map((m) => m.tieu_de));
    kiem('Dự phòng: tiêu đề giữ nguyên bản gốc, tin Anh có ngon_ngu=en, Telegram có cảnh báo', n.tin.every((m: any) => goc.has(m.tieu_de)) && n.tin.some((m: any) => m.ngon_ngu === 'en' && !m.ai) && tgText().includes('chưa dịch/tóm tắt được') && /429/.test(hang().loi || ''));
  }
}
datLai({ khongKhoaGemini: true });
r = await goi('cron');
kiem('Thiếu secret GEMINI_API_KEY: không gọi Gemini, vẫn gửi bản dự phòng', r.s === 200 && F().gem.length === 0 && !hang().noi_dung.dung_ai && r.j.da_gui);
datLai({ gem: ['xss'] });
r = await goi('cron');
kiem('Gemini trả nội dung có thẻ HTML/link độc: Telegram được escape, link vẫn là link gốc', r.s === 200 && !/<script>|<a href="javascript/i.test(tgText()) && tgText().includes('&lt;script&gt;') && hang().noi_dung.tin.every((m: any) => linkGoc.has(m.link)));

// --- Telegram lỗi ---
datLai({ tg: '400' });
r = await goi('cron');
kiem('Telegram lỗi 400: bản tin VẪN được lưu, telegram_luc rỗng, báo lỗi, ghi vào cột loi', r.s === 200 && F().db.ban_tin.length === 1 && hang().telegram_luc === null && !r.j.da_gui && /Telegram 400/.test(r.j.loi_telegram) && /Telegram 400/.test(hang().loi), JSON.stringify(r.j));
const gemTruoc = F().gem.length; F().tgMode = 'ok';
r = await goi('cron');
kiem('Lần cron sau (Telegram ổn lại): chỉ GỬI LẠI bản đã lưu, không gọi Gemini/RSS nữa, đặt telegram_luc', r.s === 200 && !r.j.tao_moi && r.j.gui_lan_nay && F().gem.length === gemTruoc && !!hang().telegram_luc && F().tg.length >= 1);
datLai({ tg: 'net' });
r = await goi('cron');
kiem('Telegram mất mạng: không ném lỗi, bản tin vẫn lưu, báo lỗi mạng', r.s === 200 && F().db.ban_tin.length === 1 && !r.j.da_gui && /lỗi mạng/.test(r.j.loi_telegram));

// --- ban-tin-lay lỗi ---
for (const lay of ['500', 'net', '404']) {
  datLai({ lay });
  r = await goi('cron');
  const n = hang()?.noi_dung;
  kiem(`ban-tin-lay lỗi (${lay}): vẫn có bản tin với phần đầu + ghi lý do, không gọi Gemini, vẫn gửi Telegram`, r.s === 200 && n && n.tin.length === 0 && n.dau.lich.length >= 1 && n.loi_nguon.length >= 1 && F().gem.length === 0 && r.j.da_gui && tgText().includes('Hôm nay chưa lấy được tin nào'), JSON.stringify(n?.loi_nguon));
}
// --- lỗi bảng ---
datLai(); F().loiBang['select:ban_tin'] = 'relation "ban_tin" does not exist';
r = await goi('cron');
kiem('Chưa chạy SQL (bảng ban_tin thiếu): báo lỗi rõ ràng, không gọi Gemini/Telegram', r.s === 500 && /sql\/2\.9/.test(r.j.loi) && F().gem.length === 0 && F().tg.length === 0);
datLai(); F().loiBang['insert:ban_tin'] = 'permission denied for table ban_tin';
r = await goi('cron');
kiem('Lưu bản tin lỗi (thiếu GRANT): báo lỗi, KHÔNG gửi Telegram (tránh gửi mà không lưu)', r.s === 500 && /Lưu bản tin lỗi/.test(r.j.loi) && F().tg.length === 0);
datLai({ sk: [], yt: [] });
r = await goi('cron');
kiem('Không có lịch/ý tưởng: phần đầu rỗng, bản tin vẫn đủ', r.s === 200 && hang().noi_dung.dau.lich.length === 0 && Telegram_ok());
function Telegram_ok() { return tgText().includes('Hôm nay không có lịch'); }
const mo = await handler(new Request('https://gia/', { method: 'OPTIONS' }));
kiem('CORS: OPTIONS trả ok; GET bị từ chối 405', mo.status === 200 && (await handler(new Request('https://gia/', { method: 'GET' }))).status === 405);
console.log(JSON.stringify(kq));
