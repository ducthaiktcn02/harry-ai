# Yêu cầu chi tiết — Harry AI (thu ở Bước A, 2026-11-26)

## 1. Tổng quan
- Tên: **Harry AI** — trợ lý AI cá nhân.
- Người dùng: **chỉ chủ app**; đăng nhập bằng **tài khoản Google**.
- Thiết bị: **điện thoại Android** + máy tính; dữ liệu tự đồng bộ.
- Máy tính không bật 24/24 → app đặt trên mạng (GitHub + Supabase).
- Giao diện: tiếng Việt, **nền sáng, kiểu Google Calendar**. Cài được lên màn hình chính (PWA).
- Chi phí: **0 đồng/tháng**.
- Cấm: lưu mật khẩu, số thẻ, giấy tờ tuỳ thân; đưa khoá API vào mã nguồn.

## 2. Lịch cá nhân (làm đầu tiên)
- Xem theo **ngày / tuần / tháng**.
- Thêm, sửa, xoá sự kiện ngay trên lịch; **kéo thả đổi giờ**.
- **Sự kiện lặp lại** (ngày/tuần/tháng).
- **Màu theo loại việc** (vd: công việc, cá nhân, quay video).
- **Nhắc việc qua Telegram** (trước 15 phút / 1 giờ / tuỳ chỉnh).
- Google Calendar: người dùng **có dùng**, nhưng **đồng bộ để giai đoạn sau**.

## 3. Kho ý tưởng
- Ghi nhanh ý tưởng. Mỗi ý tưởng: **tiêu đề, ghi chú, trạng thái (Chưa làm / Đang làm / Đã xong), ưu tiên (Cao / Vừa / Thấp), nhãn, hạn dự kiến (không bắt buộc)**.
- Xem dạng **bảng kéo thả 3 cột** theo trạng thái, hoặc danh sách.

## 4. Bản tin buổi sáng
- Gửi lúc **8:00** mỗi ngày qua **Telegram**; bản đầy đủ xem trong app.
- **10–15 tin**, mỗi tin tóm tắt 2–3 câu + **tên báo + link bài gốc**.
- Chủ đề: Thời sự trong nước, Thế giới, Kinh tế – tài chính, Công nghệ – AI, Kinh doanh online / TMĐT, Sức khoẻ, Thể thao.
- Nguồn: VnExpress, Tuổi Trẻ, Thanh Niên, VOV, Báo Chính phủ, BBC, The Guardian, DW, NHK World.
- Tin nước ngoài dịch sang tiếng Việt. AI **chỉ dịch + tóm tắt, không viết thêm**; **gộp tin trùng**.
- Phần đầu bản tin: **lịch hôm nay, việc trễ hạn, ý tưởng để lâu** (vd quá 14 ngày chưa đụng tới).

## 5. Trợ lý gõ câu tự nhiên
- Gõ "chiều thứ 6 họp khách 3h" → AI tạo sự kiện; "ý tưởng: làm kênh review đồ bếp" → AI thêm vào kho ý tưởng. Dùng Gemini.

## 6. Để sau
- Đồng bộ 2 chiều Google Calendar.
- Quản lý công việc video affiliate (tiến độ video, lịch đăng bài, link sản phẩm, hoa hồng).

## 6b. Chốt ở Bước C
- Nhắc việc **đúng giờ (lệch ≤ ~1 phút)** → dùng bộ hẹn giờ của Supabase (pg_cron + Edge Function), không dùng GitHub Actions cho nhắc việc.
- Xoá → vào **thùng rác 30 ngày**, khôi phục được (áp dụng sự kiện + ý tưởng).
- Sửa/xoá sự kiện lặp: hỏi **chỉ lần này / lần này và các lần sau / tất cả** (như Google Calendar).
- Loại việc mặc định (tự thêm/sửa/đổi màu trong app): 🔵 Công việc · 🔴 Quay/làm video · 🟢 Cá nhân/sức khoẻ · 🟠 Gia đình · 🟣 Học tập.
- Ý tưởng "để lâu": ở cột **Chưa làm quá 14 ngày** → bản tin sáng nhắc, **tối đa 3 ý/sáng**.
- Lỗi một báo → bỏ qua, vẫn gửi bản tin, cuối bản tin ghi "Hôm nay không lấy được tin từ: …".
- Gemini hết lượt miễn phí → vẫn gửi tiêu đề + link; **tin nước ngoài để nguyên tiếng Anh** (người dùng tự đọc — đã đồng ý).
- Khoá Gemini đang dùng chung với việc dịch/viết mô tả Douyin → Harry AI phải **tiết kiệm lượt**: gộp cả bản tin vào **1–2 lần gọi/ngày**, ưu tiên model nhẹ (Flash/Flash-Lite, lượt tính riêng từng model). Phương án dự phòng: tạo khoá Gemini riêng cho Harry AI (miễn phí) để không giành lượt với Douyin.
- Mất mạng trên điện thoại → **xem** được dữ liệu đã tải; **thêm/sửa cần có mạng** (tránh lệch dữ liệu).

## 7. Dịch vụ dùng (chỉ tên, khoá để ở biến môi trường/Secrets)
GitHub (mã nguồn, Pages, Actions) · Supabase (dữ liệu, đăng nhập Google) · Gemini · Telegram bot.
