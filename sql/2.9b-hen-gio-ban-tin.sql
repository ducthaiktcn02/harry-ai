-- Giai đoạn 2.9 (phần 2): hẹn giờ gửi Bản tin sáng lúc 8:00 giờ Việt Nam (= 01:00 UTC) mỗi ngày.
-- Chạy phần này SAU KHI đã chạy sql/2.9-ban-tin.sql và đã deploy function "ban-tin-gui".
-- Thay 2 chỗ <<...>> bằng giá trị thật rồi bấm Run (đừng gửi lên chat/GitHub):
--   <<MA_NHAC>>   = đúng chuỗi bí mật bạn đã đặt cho secret CRON_KEY (giống lúc làm nhắc việc 2.5)
--   <<DUONG_DAN>> = https://nrvueainkiweuvsoivgp.supabase.co/functions/v1/ban-tin-gui
create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule('ban-tin-gui') where exists (select 1 from cron.job where jobname = 'ban-tin-gui');
select cron.schedule('ban-tin-gui', '0 1 * * *', $$
  select net.http_post(
    url := '<<DUONG_DAN>>',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-cron-key', '<<MA_NHAC>>'),
    body := '{}'::jsonb,
    timeout_milliseconds := 120000
  );
$$);
