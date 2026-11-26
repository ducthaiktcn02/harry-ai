-- Giai đoạn 2.2: bảng "chủ app" + quy tắc chỉ chủ app truy cập.
-- Dán toàn bộ vào Supabase > SQL Editor > Run.
create table if not exists public.app_owner (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);
alter table public.app_owner enable row level security;

drop policy if exists "chu_doc" on public.app_owner;
create policy "chu_doc" on public.app_owner
  for select to authenticated using (user_id = auth.uid());

-- Người đăng nhập đầu tiên tự nhận làm chủ; sau đó không ai nhận thêm được.
drop policy if exists "chu_nhan" on public.app_owner;
create policy "chu_nhan" on public.app_owner
  for insert to authenticated
  with check (user_id = auth.uid() and not exists (select 1 from public.app_owner));

-- Hàm dùng cho mọi bảng dữ liệu sau này: chỉ chủ app mới qua được.
create or replace function public.la_chu_app() returns boolean
language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.app_owner where user_id = auth.uid());
$$;
