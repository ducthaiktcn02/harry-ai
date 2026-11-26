
## 2.5 — Edge Function báo "permission denied for table su_kien" (2026-11-26)
Nguyên nhân: Supabase mới không tự cấp quyền cho vai `service_role` trên bảng tạo bằng SQL. Cách sửa: `sql/2.5c-cap-quyen.sql` (GRANT). Bài học: bảng mới nào dùng trong Edge Function cũng phải GRANT cho `service_role`.
