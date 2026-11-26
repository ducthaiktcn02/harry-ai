-- Giai đoạn 2.3: bảng Lịch (sự kiện + loại việc) + quy tắc chỉ chủ app + đồng bộ tức thì.
-- Dán toàn bộ vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)

create table if not exists public.loai_viec (
  id text primary key,
  ten text not null,
  mau text not null,
  thu_tu int not null default 0
);

create table if not exists public.su_kien (
  id uuid primary key default gen_random_uuid(),
  tieu_de text not null,
  ghi_chu text,
  bat_dau timestamptz not null,
  ket_thuc timestamptz not null,
  ca_ngay boolean not null default false,
  loai text not null default 'cv',
  xoa_luc timestamptz,            -- khác rỗng = đã vào thùng rác (làm ở 2.4)
  tao_luc timestamptz not null default now(),
  sua_luc timestamptz not null default now()
);
create index if not exists su_kien_bat_dau_idx on public.su_kien (bat_dau);

alter table public.loai_viec enable row level security;
alter table public.su_kien enable row level security;

drop policy if exists "chu_all" on public.loai_viec;
create policy "chu_all" on public.loai_viec for all to authenticated
  using (public.la_chu_app()) with check (public.la_chu_app());

drop policy if exists "chu_all" on public.su_kien;
create policy "chu_all" on public.su_kien for all to authenticated
  using (public.la_chu_app()) with check (public.la_chu_app());

grant select, insert, update, delete on public.loai_viec to authenticated;
grant select, insert, update, delete on public.su_kien to authenticated;

-- 5 loại việc mặc định
insert into public.loai_viec (id, ten, mau, thu_tu) values
  ('cv', 'Công việc', '#1a73e8', 1),
  ('vd', 'Quay/làm video', '#d50000', 2),
  ('cn', 'Cá nhân/sức khoẻ', '#0b8043', 3),
  ('gd', 'Gia đình', '#f4511e', 4),
  ('ht', 'Học tập', '#8e24aa', 5)
on conflict (id) do nothing;

-- Đồng bộ tức thì giữa các thiết bị
do $$ begin
  begin alter publication supabase_realtime add table public.su_kien; exception when duplicate_object then null; end;
  begin alter publication supabase_realtime add table public.loai_viec; exception when duplicate_object then null; end;
end $$;
