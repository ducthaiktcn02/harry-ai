-- Giai đoạn 2.5 (sửa lỗi "permission denied"): cho Edge Function (vai service_role) đọc sự kiện và ghi bảng đã gửi.
-- Dán vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)
grant usage on schema public to service_role;
grant select on public.su_kien to service_role;
grant select, insert, delete on public.nhac_da_gui to service_role;
