# Tiến độ — Harry AI

## Đang ở
**Giai đoạn 2.1 XONG và đã nghiệm thu trên iPhone thật (2026-11-26): thêm vào màn hình chính được, mở toàn màn hình.** Tiếp theo: **2.2 Supabase + đăng nhập Google**. `demo/index.html` là mẫu giao diện chuẩn để bám theo khi code (màu, bố cục, chữ).
- Kho: https://github.com/ducthaiktcn02/harry-ai (công khai) · Trang: https://ducthaiktcn02.github.io/harry-ai/ (Pages từ nhánh `main`, thư mục gốc).
- Máy đã cài `gh` (winget) và đăng nhập tài khoản `ducthaiktcn02`; đường dẫn `C:\Program Files\GitHub CLI\gh.exe` (trong Bash có thể chưa có trong PATH → dùng đường dẫn đầy đủ). git đã đặt tên/email noreply chỉ riêng kho này.
- Bằng chứng: `docs/bang-chung/2.1/trang-dien-thoai.png` (chụp khổ điện thoại, trang online) + kiểm tra manifest/service worker OK. Script: `tools/chup_bang_chung.py` (chạy `py -3.12 ...` KHÔNG dùng `-I`; dùng `channel="chrome"` vì Playwright chưa tải Chromium riêng).
- Đã kiểm chứng trên iPhone (Safari → Chia sẻ → Thêm vào MH chính). Lưu ý người dùng từng không thấy nút Chia sẻ vì mở link ngoài Safari — nhắc luôn dùng Safari.
- Demo gồm: màn đăng nhập Google, Lịch ngày/tuần/tháng (bấm ô trống tạo, kéo thả đổi giờ, sự kiện lặp ↻, xoá lặp hỏi 3 lựa chọn), Kho ý tưởng (bảng 3 cột kéo thả + danh sách, lọc ưu tiên/nhãn, cảnh báo "để lâu"), Bản tin sáng mẫu, Thùng rác 30 ngày, Cài đặt (màu loại việc), nút ✨ Trợ lý (xem trước → Đồng ý). Điện thoại: thanh menu dưới.
- Vòng góp ý 1 (người dùng đồng ý): thêm (A) khung xem trước của trợ lý sửa được trước khi Đồng ý; (B) nút "Lưu thành ý tưởng" ở mỗi tin bản tin. Đã sửa demo + roadmap (2.7, 2.9). Người dùng nói **"chốt"**.

**2.2 đang làm (2026-11-26):** người dùng đã tạo dự án Supabase (vùng auto). Project URL `https://nrvueainkiweuvsoivgp.supabase.co` + khoá publishable đã lưu ở `config.js` (công khai, được phép). Việc kế: người dùng bật Google OAuth (Google Cloud → Client ID/Secret dán vào Supabase → Authentication → Providers → Google; Secret không gửi chat) → rồi mình code màn đăng nhập + bảng + RLS.

## Vừa xong
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
Phiên mới: **2.2 Supabase + đăng nhập Google** — hướng dẫn người dùng tạo tài khoản Supabase (miễn phí) + bật đăng nhập Google; RLS chỉ chủ app; thử đăng nhập trong app đã cài trên iPhone (iOS hay lỗi OAuth ở chế độ toàn màn hình). Mỗi lần sửa code → git add/commit/push, trang tự cập nhật.

## File đọc đầu tiên
`CLAUDE.md` → `docs/tien-do.md` → `docs/roadmap.md` → `demo/index.html` (mẫu giao diện) → `docs/yeu-cau.md` khi cần chi tiết.

## Lỗi đang gặp
Chưa có.
