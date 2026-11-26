# Tiến độ — Harry AI

## Đang ở
**Giai đoạn 2.4 đã code + thử bằng dữ liệu giả xong (2026-11-26); CHỜ người dùng chạy SQL `sql/2.4-lap-thung-rac.sql` trong Supabase rồi thử thật (máy tính + iPhone) để nghiệm thu.** Sau khi nghiệm thu → **2.5 Nhắc việc qua Telegram**. `demo/index.html` là mẫu giao diện chuẩn.
- Kho: https://github.com/ducthaiktcn02/harry-ai (công khai) · Trang: https://ducthaiktcn02.github.io/harry-ai/ (Pages từ nhánh `main`, thư mục gốc).
- Máy đã cài `gh` (winget) và đăng nhập tài khoản `ducthaiktcn02`; đường dẫn `C:\Program Files\GitHub CLI\gh.exe` (trong Bash có thể chưa có trong PATH → dùng đường dẫn đầy đủ). git đã đặt tên/email noreply chỉ riêng kho này.
- Bằng chứng: `docs/bang-chung/2.1/trang-dien-thoai.png` (chụp khổ điện thoại, trang online) + kiểm tra manifest/service worker OK. Script: `tools/chup_bang_chung.py` (chạy `py -3.12 ...` KHÔNG dùng `-I`; dùng `channel="chrome"` vì Playwright chưa tải Chromium riêng).
- Đã kiểm chứng trên iPhone (Safari → Chia sẻ → Thêm vào MH chính). Lưu ý người dùng từng không thấy nút Chia sẻ vì mở link ngoài Safari — nhắc luôn dùng Safari.
- Demo gồm: màn đăng nhập Google, Lịch ngày/tuần/tháng (bấm ô trống tạo, kéo thả đổi giờ, sự kiện lặp ↻, xoá lặp hỏi 3 lựa chọn), Kho ý tưởng (bảng 3 cột kéo thả + danh sách, lọc ưu tiên/nhãn, cảnh báo "để lâu"), Bản tin sáng mẫu, Thùng rác 30 ngày, Cài đặt (màu loại việc), nút ✨ Trợ lý (xem trước → Đồng ý). Điện thoại: thanh menu dưới.
- Vòng góp ý 1 (người dùng đồng ý): thêm (A) khung xem trước của trợ lý sửa được trước khi Đồng ý; (B) nút "Lưu thành ý tưởng" ở mỗi tin bản tin. Đã sửa demo + roadmap (2.7, 2.9). Người dùng nói **"chốt"**.

**2.2 đã làm:** Supabase `https://nrvueainkiweuvsoivgp.supabase.co` + Google OAuth (Client ID trong Google Cloud project `harry-ai`, chế độ Testing, Gmail chủ app trong Test users; token có thể hết hạn ~7 ngày → đăng nhập lại). Chủ app = tài khoản đầu tiên đăng nhập, lưu ở bảng `app_owner`; SQL `sql/2.2-chu-app.sql` (đã chạy, gồm GRANT cho `authenticated`). **Mọi bảng dữ liệu sau này: bật RLS, policy dùng `public.la_chu_app()`, và nhớ GRANT cho `authenticated`** (Supabase mới không tự cấp). Config công khai ở `config.js` (sw.js cache v3). Bằng chứng: `docs/bang-chung/2.2/nguoi-la-bi-chan.txt`. Trang đăng nhập hiện ở `index.html` (supabase-js qua CDN).

## Vừa xong
- **2.4 (code xong, chưa nghiệm thu thật):** kéo thả đổi giờ/ngày trong lịch tuần/ngày (chuột kéo luôn; iPhone nhấn giữ ~0,35s rồi kéo; lưới 15 phút); sự kiện lặp ngày/tuần/tháng + "lặp đến hết ngày" (tuỳ chọn), hiện ký hiệu ↻; sửa/xoá/kéo sự kiện lặp hỏi 3 lựa chọn (chỉ này / này và sau / tất cả); thùng rác 30 ngày (khôi phục, xoá hẳn, tự dọn khi mở app; mở từ menu trái hoặc ⚙ Cài đặt). Cách lưu lặp: cột `lap`, `lap_den`, `lap_ngoai` (các lần bị bỏ) trên `su_kien`; "chỉ lần này" = thêm ngoại lệ + tạo sự kiện lẻ mới; "này và sau" = cắt `lap_den` + tạo chuỗi mới. Chưa làm: kéo thả ở lịch tháng, kéo đổi độ dài (có thể thêm nếu người dùng muốn). Bằng chứng: `docs/bang-chung/2.4/` + `tools/thu_lap_gia.py` (Supabase giả nhớ trong bộ nhớ, 17 kiểm tra đều ĐẠT). sw.js cache v5.
- Bước A: thu yêu cầu. Bước B: tạo `CLAUDE.md`, `docs/yeu-cau.md`, `.env.example`, `.gitignore` (thư mục `.claude/rules` bị chặn quyền ghi → quy tắc bảo mật nằm trong `CLAUDE.md`).
- Bước C: 2 vòng phỏng vấn + câu hỏi về lượt Gemini; người dùng nói **"chốt"**.

## Đã quyết định (chọn gì — vì sao — bỏ gì)
- Lưu trữ: GitHub (code, Pages) + Supabase (dữ liệu, đăng nhập Google, đồng bộ tức thì) — an toàn, miễn phí — bỏ "chỉ dùng GitHub lưu dữ liệu" (ghi đè, lộ dữ liệu, phải để token trên điện thoại).
- Chi phí 0 đồng. Chỉ 1 người dùng, đăng nhập Google.
- Nhắc việc đúng giờ (≤ ~1 phút) bằng hẹn giờ của Supabase — bỏ GitHub Actions cho nhắc việc vì trễ 5–15 phút. Bản tin 8:00 có thể dùng GitHub Actions hoặc Supabase (chọn ở Bước D, ưu tiên gom về Supabase cho đơn giản).
- Bản tin 8:00 qua Telegram + trong app; 7 chủ đề; 10–15 tin; 9 báo; chỉ dịch+tóm tắt, gộp trùng; phần đầu: lịch hôm nay, trễ hạn, ý tưởng để lâu.
- Gemini dùng chung khoá với việc Douyin → gộp bản tin 1–2 lần gọi/ngày, model nhẹ (Flash/Flash-Lite); hết lượt → tin nước ngoài để nguyên tiếng Anh (người dùng đồng ý); dự phòng: khoá Gemini riêng.
- Lịch: ngày/tuần/tháng, kéo thả, lặp lại (sửa hỏi 3 lựa chọn như Google Calendar), 5 loại màu mặc định, nhắc qua Telegram, thùng rác 30 ngày.
- Kho ý tưởng: tiêu đề, ghi chú, trạng thái 3 mức, ưu tiên 3 mức, nhãn, hạn (tuỳ chọn); bảng kéo thả 3 cột + danh sách; "để lâu" = Chưa làm > 14 ngày, nhắc tối đa 3/sáng.
- Trợ lý gõ câu tự nhiên → tạo sự kiện/ý tưởng (Gemini).
- Mất mạng: xem được dữ liệu đã tải, thêm/sửa cần mạng.
- Điện thoại iPhone (iOS, đổi từ Android ngày 2026-11-26 — PWA phải mở bằng Safari; khi làm 2.2 phải thử đăng nhập Google trong app đã cài vì iOS hay lỗi; nhắc việc dùng Telegram nên không cần push iOS); giao diện nền sáng kiểu Google Calendar; PWA.
- Để sau: đồng bộ Google Calendar; quản lý video affiliate.
- Thứ tự làm: Lịch → Kho ý tưởng → Bản tin sáng → (sau) công việc affiliate.

## Chưa chắc chắn
- Giới hạn gói miễn phí Gemini/Supabase cụ thể — kiểm chứng khi code (dự kiến đủ cho 1 người).
- Một số báo (Báo Chính phủ, VOV, NHK) có còn RSS không — kiểm chứng ở giai đoạn bản tin.
- Giả định: kho GitHub công khai (để Pages miễn phí); dữ liệu riêng chỉ nằm ở Supabase.
- Người dùng chưa có tài khoản Supabase? (hỏi khi bắt đầu code; hướng dẫn tạo).

## Bước tiếp theo
1. Người dùng dán `sql/2.4-lap-thung-rac.sql` vào Supabase SQL Editor → Run; mở app (xoá cache/đóng mở lại), thử: kéo sự kiện, tạo sự kiện lặp, xoá lặp (3 lựa chọn), thùng rác khôi phục, trên cả máy tính và iPhone. Có lỗi → ghi `docs/loi-da-gap.md`, sửa.
2. Khi nghiệm thu "ok": tick 2.4 trong roadmap, rồi làm **2.5 Nhắc việc qua Telegram** (pg_cron mỗi phút + Edge Function; cần thêm cột nhắc trước vào `su_kien`; lưu ý sự kiện lặp phải được bung ra khi kiểm tra nhắc).

## File đọc đầu tiên
`CLAUDE.md` → `docs/tien-do.md` → `docs/roadmap.md` → `demo/index.html` (mẫu giao diện) → `docs/yeu-cau.md` khi cần chi tiết.

## Lỗi đang gặp
Chưa có.
