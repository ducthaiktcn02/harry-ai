-- Giai đoạn 2.9: bảng lưu Bản tin sáng (mỗi ngày 1 dòng) + quy tắc chỉ chủ app + đồng bộ tức thì.
-- Dán toàn bộ vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)

create table if not exists public.ban_tin (
  ngay date primary key,                         -- ngày giờ Việt Nam
  noi_dung jsonb not null,                       -- phần đầu + các tin đã dịch/tóm tắt
  tao_luc timestamptz not null default now(),
  telegram_luc timestamptz,                      -- khác rỗng = đã gửi Telegram
  loi text                                       -- ghi chú lỗi (Telegram/Gemini) nếu có
);

alter table public.ban_tin enable row level security;

drop policy if exists "chu_all" on public.ban_tin;
create policy "chu_all" on public.ban_tin for all to authenticated
  using (public.la_chu_app()) with check (public.la_chu_app());

-- Supabase mới không tự cấp quyền: app chỉ đọc; Edge Function (service_role) ghi
grant select on public.ban_tin to authenticated;
grant usage on schema public to service_role;
grant select, insert, update, delete on public.ban_tin to service_role;

-- Đồng bộ tức thì giữa các thiết bị
do $$ begin
  begin alter publication supabase_realtime add table public.ban_tin; exception when duplicate_object then null; end;
end $$;
