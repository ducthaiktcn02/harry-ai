# Hướng dẫn bật thông báo đẩy (2.5b) — làm 1 lần

Sau khi làm xong, nhắc việc sẽ hiện thành thông báo ngay trên iPhone **và** Telegram vẫn gửi song song (dự phòng).

## Bước 1. Tạo bảng lưu thiết bị (SQL)
1. Mở link này, chọn hết (Ctrl+A) rồi sao chép (Ctrl+C): https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/sql/2.5d-push.sql
2. Vào Supabase → **SQL Editor** → dán → bấm **Run**. Báo "Success" là xong (chạy lại cũng không sao).

## Bước 2. Thêm 3 "Secrets" (khoá thông báo)
Giá trị nằm trong file **`F:\Apps\harry-ai\.env`** trên máy tính này (mở bằng Notepad; **đừng dán giá trị vào chat hay đưa lên GitHub**).
1. Supabase → **Edge Functions** → **Secrets** (hoặc Project Settings → Edge Functions → Secrets).
2. Thêm lần lượt 3 dòng, tên giống hệt, giá trị copy từ file `.env`:
   - `VAPID_PUBLIC_KEY`
   - `VAPID_PRIVATE_KEY`
   - `VAPID_SUBJECT`
3. Bấm **Save**. (Các secrets cũ `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, `CRON_KEY` giữ nguyên.)

## Bước 3. Cập nhật lại function `nhac-viec`
1. Mở link, chọn hết, sao chép: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/functions/nhac-viec/index.ts
2. Supabase → **Edge Functions** → **nhac-viec** → tab **Code** → xoá hết mã cũ, dán mã mới → bấm **Deploy updates**.
3. Giữ nguyên **Verify JWT = TẮT** cho function này (như lần làm 2.5).

## Bước 4. Bật trên iPhone
1. Đợi ~2 phút sau khi mình đẩy code mới. Trên iPhone, **mở app Harry AI từ biểu tượng ngoài màn hình chính** (phải là bản đã "Thêm vào màn hình chính" bằng Safari; cần iOS 16.4 trở lên. Mở bằng Safari thường sẽ KHÔNG bật được).
2. Vào **Cài đặt** → hộp **Thông báo trên điện thoại** → bấm **Bật thông báo** → chọn **Cho phép**.
3. Bấm **Gửi thử** → vài giây sau iPhone hiện thông báo "Harry AI". Thấy là thành công.
4. Muốn thử nhắc thật: tạo sự kiện, đặt "Nhắc đúng giờ", đợi tới giờ.

## Nếu có trục trặc
- Hộp báo "Chưa dùng được": bạn đang mở bằng Safari thường → mở từ biểu tượng ngoài màn hình chính.
- Hộp báo "Đã bị chặn": iPhone → Cài đặt → Thông báo → Harry AI → Cho phép.
- Bấm Bật báo "đã chạy sql/2.5d-push.sql chưa?": quay lại Bước 1.
- Gửi thử báo 403/404: chưa làm Bước 3 (hoặc chưa Deploy).
- Gửi thử "không có thiết bị nào" / "Chưa đặt secrets VAPID": quay lại Bước 2 (tên secrets phải đúng từng chữ).
- Vẫn không được: Telegram vẫn nhắc bình thường; báo mình để xem log của function (Edge Functions → nhac-viec → Logs).
