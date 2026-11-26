-- Giai đoạn 2.5: nhắc việc qua Telegram.
-- Dán vào Supabase > SQL Editor > Run. (Chạy lại nhiều lần vẫn an toàn.)
-- Phần 1: cột nhắc + bảng ghi lần đã gửi (để không nhắc trùng).
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

-- Phần 2: hẹn giờ mỗi phút gọi Edge Function. Chạy phần này SAU KHI đã tạo function "nhac-viec".
-- Thay 2 chỗ <<...>> bằng giá trị thật rồi bấm Run (đừng gửi lên chat/GitHub):
--   <<MA_NHAC>>  = chuỗi bí mật bạn tự đặt (vd 24 ký tự ngẫu nhiên), giống hệt secret CRON_KEY của function
--   <<DUONG_DAN>> = https://nrvueainkiweuvsoivgp.supabase.co/functions/v1/nhac-viec
create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule('nhac-viec') where exists (select 1 from cron.job where jobname = 'nhac-viec');
select cron.schedule('nhac-viec', '* * * * *', $$
  select net.http_post(
    url := '<<DUONG_DAN>>',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-cron-key', '<<MA_NHAC>>'),
    body := '{}'::jsonb
  );
$$);
