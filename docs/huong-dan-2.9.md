# Hướng dẫn bật "Bản tin sáng" (2.9) — làm 1 lần

Sau khi làm xong: mỗi sáng **8:00** Telegram nhận bản tin (lịch hôm nay, việc trễ hạn, ý tưởng để lâu, 10–15 tin đã dịch + tóm tắt, kèm tên báo + link). Trong app có mục **📰 Bản tin** để xem lại các ngày trước và bấm **"💡 Lưu thành ý tưởng"** cho tin nào hay.

Không cần thêm secret mới (đã có `CRON_KEY`, `GEMINI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID` từ các bước trước). Tổng cộng 4 việc, theo đúng thứ tự dưới đây.

## Bước 1. Tạo bảng lưu bản tin (SQL)
1. Mở link, chọn hết (Ctrl+A), sao chép (Ctrl+C): https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/sql/2.9-ban-tin.sql
2. Supabase → **SQL Editor** → **New query** → dán → bấm **Run**. Thấy "Success" là xong (chạy lại nhiều lần vẫn an toàn).

## Bước 2. Tạo function `ban-tin-lay` (lấy tin từ các báo — việc còn dang dở của 2.8)
Chỉ cần **1 file duy nhất** (đã gộp sẵn, không thêm file phụ):
1. Supabase → **Edge Functions** → **Deploy a new function** (Via Editor) → đặt tên đúng là `ban-tin-lay`.
2. Mở link, chọn hết (Ctrl+A), sao chép (Ctrl+C): https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/dan-mot-file/ban-tin-lay.ts
3. Dán đè toàn bộ file `index.ts` trong trình soạn thảo (xoá sạch code mẫu trước), bấm **Deploy**.
4. Vào function `ban-tin-lay` → **Details/Settings** → **TẮT "Verify JWT"**.

## Bước 3. Tạo function `ban-tin-gui` (dịch/tóm tắt + lưu + gửi Telegram)
Cũng **1 file duy nhất**; function tự gọi `ban-tin-lay` qua mạng nên không cần liên kết gì giữa hai function.
1. Supabase → **Edge Functions** → **Deploy a new function** (Via Editor) → đặt tên đúng là `ban-tin-gui`.
2. Mở link, Ctrl+A, Ctrl+C: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/dan-mot-file/ban-tin-gui.ts
3. Dán đè toàn bộ `index.ts`, bấm **Deploy**.
4. Vào function `ban-tin-gui` → **Details/Settings** → **TẮT "Verify JWT"**.

## Bước 4. Thử bằng nút trong app (chưa gửi Telegram)
1. Đợi ~2 phút sau khi mình đẩy code, mở app (iPhone: mở từ biểu tượng ngoài màn hình chính; máy tính: Ctrl+Shift+R).
2. Bấm mục **📰 Bản tin** → bấm **Tạo bản tin hôm nay** → chờ khoảng 20–60 giây.
3. Thấy bản tin hiện ra là đúng. Kiểm tra: có phần "Lịch hôm nay / Việc trễ hạn / Ý tưởng để lâu", các tin có tên báo (bấm mở bài gốc), bấm thử **💡 Lưu thành ý tưởng** rồi sang **Kho ý tưởng** xem có thẻ nhãn `từ bản tin`.
4. Nếu dòng trên cùng ghi "chưa dịch/tóm tắt được" nghĩa là Gemini hôm nay hết lượt hoặc lỗi → bản tin vẫn có, tin nước ngoài để tiếng Anh (đúng như đã thống nhất).

## Bước 5. Đặt hẹn giờ 8:00 sáng mỗi ngày
1. Mở link, sao chép: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/sql/2.9b-hen-gio-ban-tin.sql
2. Supabase → **SQL Editor** → **New query** → dán. **Thay 2 chỗ** trước khi Run (đừng gửi nội dung đã thay lên chat/GitHub):
   - `<<MA_NHAC>>` → đúng chuỗi bí mật bạn đã đặt cho secret `CRON_KEY` ở bước nhắc việc (2.5) — chuỗi này cũng đang nằm trong câu lệnh hẹn giờ cũ `nhac-viec` (SQL Editor → chạy `select command from cron.job where jobname = 'nhac-viec';` để xem lại).
   - `<<DUONG_DAN>>` → `https://nrvueainkiweuvsoivgp.supabase.co/functions/v1/ban-tin-gui`
3. Bấm **Run**. (Hẹn giờ này chạy lúc 01:00 UTC = 8:00 giờ Việt Nam.)

## Bước 6 (tuỳ chọn). Gửi thử Telegram ngay, không đợi tới 8:00
Trong SQL Editor, chạy (thay 2 chỗ như Bước 5):
```
select net.http_post(url := '<<DUONG_DAN>>', headers := jsonb_build_object('Content-Type','application/json','x-cron-key','<<MA_NHAC>>'), body := '{}'::jsonb, timeout_milliseconds := 120000);
```
Vài chục giây sau Telegram nhận bản tin. Lưu ý: hôm nay đã gửi rồi nên 8:00 sáng mai mới gửi tiếp (mỗi ngày chỉ gửi 1 lần, tránh trùng).

## Nghiệm thu
Bản tin đến Telegram **đúng 8:00 hai ngày liên tiếp** → nhắn mình "chốt 2.9". Nếu 8:00 không thấy tin: vào app → 📰 Bản tin xem hôm nay đã có bản chưa (có → lỗi ở Telegram; chưa có → lỗi ở hẹn giờ/function); Supabase → Edge Functions → `ban-tin-gui` → **Logs**.

## Nếu có trục trặc
- "Chưa cài bản tin (chưa deploy function ban-tin-gui)": chưa làm Bước 3 hoặc đặt sai tên.
- "Đọc bảng ban_tin lỗi … đã chạy sql/2.9-ban-tin.sql chưa?": chưa làm Bước 1.
- Bản tin chỉ có phần đầu, ghi "ban-tin-lay trả lỗi 404": chưa làm Bước 2.
- "Chỉ chủ app được tạo bản tin": đăng nhập lại bằng đúng tài khoản Google chủ app.
- Telegram không nhận nhưng app có bản tin: kiểm tra secret `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`; bản tin chưa gửi sẽ được **gửi lại ở lần hẹn giờ kế tiếp** (cột "Chưa gửi qua Telegram" hiện ở đầu trang Bản tin). Muốn gửi lại ngay: chạy câu lệnh ở Bước 6.
- Muốn tạo lại bản tin hôm nay (vd sửa nguồn báo): bấm **Tạo lại bản tin hôm nay** trong app (tốn thêm 1 lượt Gemini, không gửi lại Telegram).
