
## 2.5 — Edge Function báo "permission denied for table su_kien" (2026-11-26)
Nguyên nhân: Supabase mới không tự cấp quyền cho vai `service_role` trên bảng tạo bằng SQL. Cách sửa: `sql/2.5c-cap-quyen.sql` (GRANT). Bài học: bảng mới nào dùng trong Edge Function cũng phải GRANT cho `service_role`.

- 2.7 (2026-11-26): trợ lý báo 'Gemini đang bận' vì model `gemini-2.5-flash-lite` đã bị Google gỡ (404). Đổi sang `gemini-3.5-flash-lite`, tách riêng thông báo 404, bắt buộc điền mọi trường trong schema (không thì model bỏ sót ngày/giờ). Lần sau: kiểm model bằng 1 lệnh gọi thật trước khi deploy.
