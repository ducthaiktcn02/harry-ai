# Harry AI — trợ lý AI cá nhân

App web cho **một người dùng** (chủ app), dùng trên điện thoại iPhone (iOS) và máy tính, dữ liệu tự đồng bộ. Giao diện **100% tiếng Việt**, kiểu Google Calendar (nền sáng).

Chi tiết yêu cầu: `docs/yeu-cau.md` · Tiến độ/bàn giao: `docs/tien-do.md` · Lộ trình: `docs/roadmap.md` (tạo ở Bước D).

## Công nghệ đã chọn (dự kiến, chốt ở Bước C/D)
- Giao diện: web app PWA (cài lên màn hình chính), đăng trên **GitHub Pages**.
- Dữ liệu + đăng nhập Google + đồng bộ tức thì: **Supabase** (gói miễn phí).
- Việc chạy theo giờ: nhắc việc dùng **hẹn giờ của Supabase** (đúng giờ ≤ ~1 phút); bản tin 8:00 cũng chạy trên Supabase (đã chốt ở Bước D). Lộ trình: `docs/roadmap.md`.
- AI (dịch/tóm tắt tin, hiểu câu tự nhiên): **Gemini** (khoá `GEMINI_API_KEY` có sẵn, **dùng chung với việc Douyin** → tiết kiệm lượt: bản tin 1–2 lần gọi/ngày, model nhẹ; hết lượt thì để tin tiếng Anh).
- Thông báo: **Telegram bot** (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` có sẵn).
- Chi phí: **0 đồng/tháng** — chỉ dùng gói miễn phí.

## Quy tắc cốt lõi
1. Trả lời người dùng bằng tiếng Việt, đơn giản (người dùng không biết code).
2. **Không viết code khi chưa duyệt roadmap + demo.** Làm từng giai đoạn nhỏ.
3. Xong mỗi tính năng phải **chạy thật và nộp bằng chứng** (ảnh chụp/log) trước khi báo xong.
4. **Không in, không hardcode khoá API** — đọc từ biến môi trường / `.env` / GitHub Secrets. Kho code là công khai.
5. Dữ liệu chỉ chủ app đọc/ghi được (bảo vệ bằng quy tắc truy cập của Supabase theo tài khoản Google).
6. Không lưu mật khẩu, số thẻ, giấy tờ tuỳ thân.
7. Bản tin: AI chỉ dịch + tóm tắt, **không viết thêm**; mỗi tin có tên báo + link gốc; gộp tin trùng.
8. Gặp lỗi → ghi vào `docs/loi-da-gap.md`.
9. Giờ: múi giờ Việt Nam (Asia/Ho_Chi_Minh).

## Phạm vi
- **Bản đầu (theo thứ tự):** Lịch → Kho ý tưởng → Bản tin sáng (+ trợ lý gõ câu tự nhiên).
- **Để sau:** đồng bộ 2 chiều Google Calendar; quản lý video affiliate (tiến độ video, lịch đăng, link sản phẩm, hoa hồng).
