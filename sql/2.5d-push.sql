-- Giai đoạn 2.5b: nơi lưu "địa chỉ nhận thông báo đẩy" của các thiết bị (iPhone, máy tính).
-- Dán toàn bộ vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)
create table if not exists public.push_dang_ky (
  id uuid primary key default gen_random_uuid(),
  endpoint text not null unique,
  p256dh text not null,
  auth text not null,
  tao_luc timestamptz not null default now(),
  ua text
);

alter table public.push_dang_ky enable row level security;

drop policy if exists "chu_all" on public.push_dang_ky;
create policy "chu_all" on public.push_dang_ky for all to authenticated
  using (public.la_chu_app()) with check (public.la_chu_app());

-- Supabase mới không tự cấp quyền: cấp cho người dùng đăng nhập VÀ cho Edge Function (service_role)
grant select, insert, update, delete on public.push_dang_ky to authenticated;
grant usage on schema public to service_role;
grant select, insert, update, delete on public.push_dang_ky to service_role;
