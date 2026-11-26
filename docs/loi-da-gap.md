
## 2.5 — Edge Function báo "permission denied for table su_kien" (2026-11-26)
Nguyên nhân: Supabase mới không tự cấp quyền cho vai `service_role` trên bảng tạo bằng SQL. Cách sửa: `sql/2.5c-cap-quyen.sql` (GRANT). Bài học: bảng mới nào dùng trong Edge Function cũng phải GRANT cho `service_role`.

- 2.7 (2026-11-26): trợ lý báo 'Gemini đang bận' vì model `gemini-2.5-flash-lite` đã bị Google gỡ (404). Đổi sang `gemini-3.5-flash-lite`, tách riêng thông báo 404, bắt buộc điền mọi trường trong schema (không thì model bỏ sót ngày/giờ). Lần sau: kiểm model bằng 1 lệnh gọi thật trước khi deploy.

## 2.8 — Lấy tin RSS (2026-11-26)
- VOV: địa chỉ RSS cũ có số (`chinh-tri-212.rss`…) đã chết (404); dùng dạng mới không số lấy từ vov.vn/rss.html. `doanh-nghiep.rss` có trong danh sách nhưng cũng 404.
- NHK World: RSS tiếng Anh không còn (404 mọi đường dẫn); feed tiếng Nhật và all.json đều cũ → bỏ NHK khỏi bản tin.
- DW: `rss-en-sci`, `rss-en-sport` trả HTML, chỉ dùng `rss-en-world`, `rss-en-bus`.
- Tuổi Trẻ / Báo Chính phủ ghi ngày kiểu `11/26/2026 7:23:00 PM` (giờ VN) → lần đầu bị coi là "không có ngày"; đã thêm bộ đọc riêng. Thanh Niên thỉnh thoảng cắt kết nối giữa chừng (IncompleteRead) → tải thử lại 1 lần.
- Không báo nào có RSS riêng cho TMĐT → lọc từ khoá từ mục kinh tế; ban đầu cắt 15 tin mới nhất TRƯỚC khi lọc nên gần như ra 0 tin TMĐT → đã sửa cắt sau khi lọc; từ khoá "amazon" bắt nhầm rừng Amazon → chỉ còn amazon.com/prime/seller. Chủ đề TMĐT vẫn mỏng (~2 tin/ngày).
- Máy chưa có Deno → đã cài `winget install DenoLand.Deno` (v2.9.8) để chạy test TypeScript; trong Git Bash cần mở shell mới (hoặc gọi đường dẫn đầy đủ trong thư mục WinGet\Packages).

## 2.9 — Bản tin dịch/tóm tắt (2026-11-26)
- Dashboard Supabase không cho import chéo thư mục (`../ban-tin-lay/`) → `ban-tin-gui` gọi HTTP `ban-tin-lay` thay vì import, mỗi function tự đủ file.
- Trang Bản tin tải bảng `ban_tin` lười (chỉ khi mở trang), vì các bộ test giả cũ không có bảng này và sẽ vỡ nếu tải ngay khi vào app. Thanh menu dưới điện thoại từ 3 → 4 mục nên `tools/thu_y_tuong_gia.py` đã sửa kiểm tra 3 → 4.
- Test giao diện: Supabase giả khai báo `const luu` trùng tên hàm `luu()` của app → "Identifier 'luu' has already been declared" làm app không mở; đặt tên giả bắt đầu bằng `__`.
- Lần chạy Gemini thật đầu tiên báo "Không kết nối được tới Gemini" (lỗi mạng thoáng qua; GET kiểm tra vẫn 200, lần sau OK). Đã ghi lý do lỗi mạng vào thông báo cho dễ chẩn đoán.
- Lần chạy Gemini thật: model chỉ chọn tin tiếng Việt, bỏ báo nước ngoài → thêm yêu cầu "trộn báo trong/ngoài nước, Thế giới ≥ 1 tin tiếng Anh" vào prompt (chưa kiểm lại với Gemini thật).
- Lỗi nhẹ chưa sửa: nếu `ban_tin` có bản tin tạo bằng nút lúc rất sớm (vd 0:10) thì 8:00 vẫn gửi bản cũ đó; chưa giới hạn tần suất bấm "Tạo lại".


## 2.9 — Deploy lỗi "Module not found .../source/nguon.ts" (2026-11-26)
- Nguyên nhân: trình soạn thảo web Supabase không giữ file thứ hai (nguon.ts/loi.ts) nên import `./nguon.ts` không thấy.
- Cách sửa: `tools/gop_mot_file.py` gộp thành 1 file ở `supabase/dan-mot-file/` (deno check ĐẠT); hướng dẫn 2.9 dùng 2 file này. Sửa code function → chạy lại script gộp.
