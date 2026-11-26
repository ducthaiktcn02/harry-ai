# Hướng dẫn bật "Lấy tin" (2.8) — làm 1 lần

Giai đoạn này chỉ lấy tin thô từ các báo (chưa dịch, chưa gửi Telegram — đó là 2.9). Bạn chỉ cần tạo 1 function mới trên Supabase. **Không cần thêm secret nào** (RSS các báo là công khai, không dùng khoá).

## Bước 1. Tạo function `ban-tin-lay`
Function gồm 3 file nhỏ; trong Supabase bạn dán từng file một:

1. Supabase → **Edge Functions** → **Deploy a new function** (Via Editor) → đặt tên đúng là `ban-tin-lay`.
2. Trình soạn thảo mặc định có file `index.ts`. Mở link này, chọn hết (Ctrl+A), sao chép (Ctrl+C), dán đè vào `index.ts`: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/functions/ban-tin-lay/index.ts
3. Bấm dấu **+** (thêm file) trong trình soạn thảo, đặt tên `nguon.ts`, rồi dán nội dung từ: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/functions/ban-tin-lay/nguon.ts
4. Thêm tiếp file `loi.ts`, dán nội dung từ: https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/functions/ban-tin-lay/loi.ts
5. Bấm **Deploy**.
6. Vào function `ban-tin-lay` → **Details/Settings** → **TẮT "Verify JWT"** (giống `nhac-viec`, `tro-ly`; function tự kiểm bạn có phải chủ app hay không).

> Nếu trình soạn thảo trên web không cho thêm file (chỉ có 1 file), nhắn mình — mình sẽ gộp 3 file thành 1 cho bạn dán.

## Bước 2. Thử (không bắt buộc ở giai đoạn này)
Trong Supabase → function `ban-tin-lay` → tab **Test/Invoke** hoặc dùng sau này ở 2.9. Kết quả đúng sẽ là một khối chữ có `tin` (7 chủ đề), `loi` (các báo không lấy được hôm nay) và `dem` (số lượng). Máy tính của mình đã chạy thử đúng phần lấy tin này: xem https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/docs/bang-chung/2.8/tin-tho.txt (sau khi mình đẩy code lên).

## Nếu có trục trặc
- Báo "Chỉ chủ app được lấy tin": đăng nhập lại bằng đúng tài khoản Google chủ app.
- `loi` có tên một báo: báo đó hôm nay tải không được — cứ bỏ qua, các báo khác vẫn ra tin.
- Báo đổi địa chỉ RSS: sửa trong file `nguon.ts` (chạy `py -3.12 tools/kiem_rss.py` để kiểm lại các địa chỉ).
- NHK World đã bỏ vì không còn RSS (xem `docs/bang-chung/2.8/nguon-chot.md`).
