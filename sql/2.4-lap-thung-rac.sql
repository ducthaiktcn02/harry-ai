-- Giai đoạn 2.4: sự kiện lặp lại (ngày/tuần/tháng) + ngoại lệ. Thùng rác dùng cột xoa_luc đã có ở 2.3.
-- Dán toàn bộ vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)

alter table public.su_kien add column if not exists lap text not null default 'none';
alter table public.su_kien add column if not exists lap_den date;                       -- lặp tới hết ngày này (rỗng = mãi mãi)
alter table public.su_kien add column if not exists lap_ngoai timestamptz[] not null default '{}'; -- các lần lặp bị bỏ ("chỉ sự kiện này")

alter table public.su_kien drop constraint if exists su_kien_lap_check;
alter table public.su_kien add constraint su_kien_lap_check check (lap in ('none', 'day', 'week', 'month'));
