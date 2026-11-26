-- Giai đoạn 2.5 (phần 2): hẹn giờ mỗi phút.
-- hẹn giờ mỗi phút gọi Edge Function. Chạy phần này SAU KHI đã tạo function "nhac-viec".
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
