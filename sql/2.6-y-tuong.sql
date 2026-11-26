-- Giai đoạn 2.6: bảng Kho ý tưởng + quy tắc chỉ chủ app + đồng bộ tức thì.
-- Dán toàn bộ vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)

create table if not exists public.y_tuong (
  id uuid primary key default gen_random_uuid(),
  tieu_de text not null,
  ghi_chu text,
  trang_thai text not null default 'chua_lam',   -- chua_lam | dang_lam | xong
  uu_tien text not null default 'vua',           -- cao | vua | thap
  nhan text[] not null default '{}',
  han date,                                       -- hạn dự kiến (không bắt buộc)
  thu_tu int not null default 0,                  -- nhỏ hơn = nằm trên
  tao_luc timestamptz not null default now(),
  sua_luc timestamptz not null default now(),     -- "để lâu" tính từ lần sửa/kéo gần nhất
  xoa_luc timestamptz,                            -- khác rỗng = đã vào thùng rác 30 ngày
  nguon text,                                     -- vd tên báo (ý tưởng lưu từ bản tin, làm ở 2.9)
  link text
);

alter table public.y_tuong drop constraint if exists y_tuong_trang_thai_check;
alter table public.y_tuong add constraint y_tuong_trang_thai_check check (trang_thai in ('chua_lam', 'dang_lam', 'xong'));
alter table public.y_tuong drop constraint if exists y_tuong_uu_tien_check;
alter table public.y_tuong add constraint y_tuong_uu_tien_check check (uu_tien in ('cao', 'vua', 'thap'));

create index if not exists y_tuong_trang_thai_idx on public.y_tuong (trang_thai, thu_tu);

alter table public.y_tuong enable row level security;

drop policy if exists "chu_all" on public.y_tuong;
create policy "chu_all" on public.y_tuong for all to authenticated
  using (public.la_chu_app()) with check (public.la_chu_app());

-- Supabase mới không tự cấp quyền: cấp cho người dùng đăng nhập VÀ cho Edge Function (service_role)
grant select, insert, update, delete on public.y_tuong to authenticated;
grant usage on schema public to service_role;
grant select, insert, update, delete on public.y_tuong to service_role;

-- Đồng bộ tức thì giữa các thiết bị
do $$ begin
  begin alter publication supabase_realtime add table public.y_tuong; exception when duplicate_object then null; end;
end $$;
