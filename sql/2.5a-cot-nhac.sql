-- Giai đoạn 2.5: nhắc việc qua Telegram.
-- Dán vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)
-- cột nhắc + bảng ghi lần đã gửi (để không nhắc trùng).
alter table public.su_kien add column if not exists nhac_phut int;   -- rỗng = không nhắc; 0 = đúng giờ; 15 = trước 15 phút...
alter table public.su_kien drop constraint if exists su_kien_nhac_check;
alter table public.su_kien add constraint su_kien_nhac_check check (nhac_phut is null or (nhac_phut >= 0 and nhac_phut <= 10080));

create table if not exists public.nhac_da_gui (
  su_kien_id uuid not null,
  lan timestamptz not null,              -- giờ bắt đầu của lần (với sự kiện lặp)
  gui_luc timestamptz not null default now(),
  primary key (su_kien_id, lan)
);
alter table public.nhac_da_gui enable row level security;   -- không có policy = chỉ Edge Function (service_role) đọc/ghi

