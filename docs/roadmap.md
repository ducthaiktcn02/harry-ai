# Lộ trình — Harry AI

Mỗi giai đoạn nhỏ, làm xong **chạy thử được** và nộp **bằng chứng** (ảnh chụp/log) rồi mới sang giai đoạn sau. Mỗi giai đoạn = 1 phiên làm việc.

Quyết định ở Bước D: **bản tin 8:00 chạy trên Supabase** (hẹn giờ pg_cron + Edge Function), giống nhắc việc → mọi việc chạy theo giờ gom về một chỗ. GitHub chỉ để chứa code + đăng trang (Pages).

## Giai đoạn 1 — Lên kế hoạch
- [x] A–C: thu yêu cầu, tạo file quy chuẩn, chốt chi tiết
- [x] D: roadmap (file này) — người dùng duyệt 2026-11-26
- [x] E: demo giao diện `demo/index.html` → **đã chốt 2026-11-26**, bắt đầu Giai đoạn 2

## Giai đoạn 2 — Code

### 2.1 Khung app + đưa lên mạng — ✅ XONG 2026-11-26 (nghiệm thu trên iPhone)
- Làm: tạo kho GitHub (công khai), trang PWA trống tiếng Việt, đăng lên GitHub Pages, cài được lên màn hình chính iPhone (Safari → Chia sẻ → Thêm vào MH chính).
- Xong khi: mở link trên điện thoại thấy trang "Harry AI", bấm "Thêm vào màn hình chính" được.
- Bằng chứng: link trang + ảnh chụp điện thoại.

### 2.2 Supabase + đăng nhập Google — ✅ XONG 2026-11-26 (máy tính + iPhone)
- Làm: hướng dẫn người dùng tạo tài khoản Supabase (miễn phí), bật đăng nhập Google, tạo bảng dữ liệu + **quy tắc chỉ chủ app đọc/ghi** (RLS).
- Xong khi: đăng nhập Google được trên máy tính + điện thoại; tài khoản Google khác bị chặn.
- Bằng chứng: ảnh đăng nhập thành công + ảnh/log tài khoản lạ bị từ chối.

### 2.3 Lịch — xem + thêm/sửa/xoá — ✅ XONG 2026-11-26 (nghiệm thu máy tính + iPhone)
- Làm: lịch ngày/tuần/tháng kiểu Google Calendar; thêm/sửa/xoá sự kiện; 5 loại màu mặc định (sửa được); lưu Supabase.
- Xong khi: tạo sự kiện trên máy tính → điện thoại thấy ngay (đồng bộ tức thì).
- Bằng chứng: ảnh 2 màn hình cùng sự kiện.

### 2.4 Lịch — kéo thả, lặp lại, thùng rác — ✅ XONG 2026-11-26 (nghiệm thu thật)
- Làm: kéo thả đổi giờ; sự kiện lặp ngày/tuần/tháng; sửa/xoá lặp hỏi 3 lựa chọn; thùng rác 30 ngày (khôi phục được).
- Xong khi: các thao tác trên chạy đúng, lặp hiện đúng các ngày.
- Bằng chứng: ảnh/quay màn hình từng thao tác.

### 2.5 Nhắc việc qua Telegram — ✅ XONG 2026-11-26 (tin đến đúng giờ)
- Làm: chọn nhắc trước 15 phút / 1 giờ / tuỳ chỉnh; Supabase hẹn giờ mỗi phút kiểm tra và gửi Telegram.
- Xong khi: tạo sự kiện thử, tin nhắn Telegram đến **lệch ≤ ~1 phút**.
- Bằng chứng: ảnh tin Telegram kèm giờ nhận + log.

### 2.5b Thông báo đẩy (Web Push) trên iPhone — ✅ XONG 2026-11-26 (thông báo đến iPhone thật, người dùng chốt)
- Làm: hộp "Thông báo trên điện thoại" ở Cài đặt (Bật/Tắt/Gửi thử); bảng `push_dang_ky`; service worker nhận `push`; Edge Function `nhac-viec` gửi thêm Web Push (Telegram giữ làm dự phòng, cả hai cùng gửi).
- Xong khi: bấm "Gửi thử" trên iPhone (app đã Thêm vào MH chính, iOS 16.4+) thấy thông báo; nhắc thật đến cả Telegram lẫn iPhone.
- Bằng chứng: `docs/bang-chung/2.5b/` (log giả + ảnh hộp Cài đặt); ảnh iPhone thật khi người dùng thử.

### 2.6 Kho ý tưởng — ✅ XONG 2026-11-26 (người dùng thử thật 2 thiết bị, chốt)
- Làm: thêm ý tưởng (tiêu đề, ghi chú, trạng thái, ưu tiên, nhãn, hạn); bảng kéo thả 3 cột + dạng danh sách; lọc theo nhãn/ưu tiên; thùng rác.
- Xong khi: thêm/kéo thả/sửa/xoá chạy, đồng bộ 2 thiết bị.
- Bằng chứng: ảnh bảng 3 cột + danh sách.

### 2.7 Trợ lý gõ câu tự nhiên
- Làm: ô gõ câu → Gemini (model nhẹ) hiểu → hiện bản xem trước "sẽ tạo…" **sửa được ngay** (tiêu đề, ngày, giờ, loại, nhắc / ưu tiên) → bấm Đồng ý mới lưu.
- Xong khi: "chiều thứ 6 họp khách 3h" tạo đúng sự kiện; "ý tưởng: làm kênh review đồ bếp" vào kho ý tưởng.
- Bằng chứng: ảnh trước/sau + 5 câu thử.

### 2.8 Bản tin sáng — lấy tin
- Làm: đọc RSS 9 báo, xếp vào 7 chủ đề, gộp tin trùng; kiểm chứng báo nào còn RSS (VOV, Báo Chính phủ, NHK); báo lỗi → bỏ qua và ghi tên.
- Xong khi: chạy thử ra danh sách tin thô đủ chủ đề.
- Bằng chứng: log danh sách tin + báo nào lỗi.

### 2.9 Bản tin sáng — dịch/tóm tắt + gửi 8:00
- Làm: gộp 1–2 lần gọi Gemini/ngày, chọn 10–15 tin, tóm tắt 2–3 câu + tên báo + link; phần đầu: lịch hôm nay, việc trễ hạn, tối đa 3 ý tưởng để lâu (>14 ngày); hết lượt Gemini → để tiếng Anh; gửi Telegram 8:00 + trang Bản tin trong app (xem lại các ngày trước; mỗi tin có nút **"Lưu thành ý tưởng"** → vào Kho ý tưởng, nhãn "từ bản tin", kèm tên báo + link).
- Xong khi: bản tin đến Telegram đúng 8:00 hai ngày liên tiếp.
- Bằng chứng: ảnh Telegram + trang Bản tin trong app.

### 2.10 Hoàn thiện
- Làm: xem khi mất mạng (chỉ đọc), giao diện điện thoại gọn, sửa lỗi người dùng báo sau khi dùng thử thật 3–5 ngày.
- Xong khi: người dùng dùng ổn, không còn lỗi lớn.
- Bằng chứng: danh sách lỗi đã sửa trong `docs/loi-da-gap.md`.

## Để sau (chưa làm ở bản đầu)
- Đồng bộ 2 chiều Google Calendar.
- Quản lý video affiliate (tiến độ video, lịch đăng, link sản phẩm, hoa hồng).
