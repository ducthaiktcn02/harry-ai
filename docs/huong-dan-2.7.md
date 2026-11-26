# Hướng dẫn bật Trợ lý ✨ (2.7) — làm 1 lần

Sau khi làm xong, bấm nút ✨ trong app, gõ một câu như "chiều thứ 6 họp khách 3h" → app hiện khung xem trước (sửa được) → bấm **Đồng ý** mới lưu.

## Bước 1. Thêm secret `GEMINI_API_KEY`
Giá trị là khoá Gemini có sẵn trên máy tính này (biến môi trường `GEMINI_API_KEY`; **đừng dán khoá vào chat hay đưa lên GitHub**). Cách lấy ra để dán: mở PowerShell, gõ `$env:GEMINI_API_KEY | clip` rồi Enter — khoá nằm trong bộ nhớ tạm, chỉ việc dán (Ctrl+V) vào ô Value ở bước dưới.
1. Supabase → **Edge Functions** → **Secrets** (hoặc Project Settings → Edge Functions → Secrets).
2. Thêm 1 dòng: Name = `GEMINI_API_KEY`, Value = dán khoá → **Save**.

## Bước 2. Tạo function `tro-ly`
1. Mở link, chọn hết (Ctrl+A), sao chép (Ctrl+C): https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/supabase/functions/tro-ly/index.ts
2. Supabase → **Edge Functions** → **Deploy a new function** (Via Editor) → đặt tên đúng là `tro-ly` → xoá mã mẫu, dán mã vừa chép → **Deploy**.
3. Vào function `tro-ly` → **Details/Settings** → **TẮT "Verify JWT"** (giống `nhac-viec`; function tự kiểm tra bạn có phải chủ app hay không).

## Bước 3. Thử
Đợi ~2 phút sau khi mình đẩy code mới, mở app (iPhone: mở từ biểu tượng ngoài màn hình chính; máy tính: Ctrl+Shift+R) → bấm nút ✨ (góc phải dưới) → bấm thử một câu gợi ý.

## Nếu có trục trặc
- "Chưa cài trợ lý (chưa deploy function tro-ly)": chưa làm Bước 2 hoặc đặt sai tên.
- "Chỉ chủ app được dùng trợ lý": hãy đăng nhập lại bằng đúng tài khoản Google chủ app.
- "Khoá Gemini chưa đúng…": kiểm tra lại secret `GEMINI_API_KEY` ở Bước 1.
- "Trợ lý hết lượt…": hết lượt miễn phí của Gemini trong ngày; thử lại sau hoặc tạo bằng nút **+** như cũ.
