# Tiến độ — Harry AI

## Đang ở
**Giai đoạn 1 XONG — người dùng đã CHỐT kế hoạch + demo (2026-11-26).** Tiếp theo: **Giai đoạn 2.1 (Khung app + đưa lên GitHub Pages)** theo `docs/roadmap.md`. `demo/index.html` là mẫu giao diện chuẩn để bám theo khi code (màu, bố cục, chữ).
- Lưu ý: demo chưa được chạy thử tự động (lệnh Playwright bị chặn quyền) — khi code, test bằng Playwright cần người dùng cho phép lệnh `py -3.12 ...`.
- 2.1 cần: người dùng có tài khoản GitHub chưa? (hỏi đầu phiên; nếu chưa → hướng dẫn tạo). Kiểm tra `gh` CLI đã đăng nhập chưa.
- Demo gồm: màn đăng nhập Google, Lịch ngày/tuần/tháng (bấm ô trống tạo, kéo thả đổi giờ, sự kiện lặp ↻, xoá lặp hỏi 3 lựa chọn), Kho ý tưởng (bảng 3 cột kéo thả + danh sách, lọc ưu tiên/nhãn, cảnh báo "để lâu"), Bản tin sáng mẫu, Thùng rác 30 ngày, Cài đặt (màu loại việc), nút ✨ Trợ lý (xem trước → Đồng ý). Điện thoại: thanh menu dưới.
- Vòng góp ý 1 (người dùng đồng ý): thêm (A) khung xem trước của trợ lý sửa được trước khi Đồng ý; (B) nút "Lưu thành ý tưởng" ở mỗi tin bản tin. Đã sửa demo + roadmap (2.7, 2.9). Người dùng nói **"chốt"**.

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
- Điện thoại Android; giao diện nền sáng kiểu Google Calendar; PWA.
- Để sau: đồng bộ Google Calendar; quản lý video affiliate.
- Thứ tự làm: Lịch → Kho ý tưởng → Bản tin sáng → (sau) công việc affiliate.

## Chưa chắc chắn
- Giới hạn gói miễn phí Gemini/Supabase cụ thể — kiểm chứng khi code (dự kiến đủ cho 1 người).
- Một số báo (Báo Chính phủ, VOV, NHK) có còn RSS không — kiểm chứng ở giai đoạn bản tin.
- Giả định: kho GitHub công khai (để Pages miễn phí); dữ liệu riêng chỉ nằm ở Supabase.
- Người dùng chưa có tài khoản Supabase? (hỏi khi bắt đầu code; hướng dẫn tạo).

## Bước tiếp theo
Phiên mới (chế độ Code): **Giai đoạn 2.1** — tạo kho GitHub công khai, trang PWA tiếng Việt (manifest + service worker + icon), đăng GitHub Pages; nghiệm thu: mở link trên điện thoại, "Thêm vào màn hình chính" được; nộp link + ảnh. Chỉ làm 2.1, xong hỏi chốt rồi mới sang 2.2.

## File đọc đầu tiên
`CLAUDE.md` → `docs/tien-do.md` → `docs/roadmap.md` → `demo/index.html` (mẫu giao diện) → `docs/yeu-cau.md` khi cần chi tiết.

## Lỗi đang gặp
Chưa có.
