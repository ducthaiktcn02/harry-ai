# Tiến độ — Harry AI

## Đang ở
**Giai đoạn 2.6 (Kho ý tưởng) và 2.5b (thông báo đẩy iPhone) XONG, người dùng đã thử thật và chốt (2026-11-26).** Tiếp theo: **2.7 Trợ lý gõ câu tự nhiên** (Gemini). `demo/index.html` là mẫu giao diện chuẩn.
- Kho: https://github.com/ducthaiktcn02/harry-ai (công khai) · Trang: https://ducthaiktcn02.github.io/harry-ai/ (Pages từ nhánh `main`, thư mục gốc).
- Máy đã cài `gh` (winget) và đăng nhập tài khoản `ducthaiktcn02`; đường dẫn `C:\Program Files\GitHub CLI\gh.exe` (trong Bash có thể chưa có trong PATH → dùng đường dẫn đầy đủ). git đã đặt tên/email noreply chỉ riêng kho này.
- Bằng chứng: `docs/bang-chung/2.1/trang-dien-thoai.png` (chụp khổ điện thoại, trang online) + kiểm tra manifest/service worker OK. Script: `tools/chup_bang_chung.py` (chạy `py -3.12 ...` KHÔNG dùng `-I`; dùng `channel="chrome"` vì Playwright chưa tải Chromium riêng).
- Đã kiểm chứng trên iPhone (Safari → Chia sẻ → Thêm vào MH chính). Lưu ý người dùng từng không thấy nút Chia sẻ vì mở link ngoài Safari — nhắc luôn dùng Safari.
- Demo gồm: màn đăng nhập Google, Lịch ngày/tuần/tháng (bấm ô trống tạo, kéo thả đổi giờ, sự kiện lặp ↻, xoá lặp hỏi 3 lựa chọn), Kho ý tưởng (bảng 3 cột kéo thả + danh sách, lọc ưu tiên/nhãn, cảnh báo "để lâu"), Bản tin sáng mẫu, Thùng rác 30 ngày, Cài đặt (màu loại việc), nút ✨ Trợ lý (xem trước → Đồng ý). Điện thoại: thanh menu dưới.
- Vòng góp ý 1 (người dùng đồng ý): thêm (A) khung xem trước của trợ lý sửa được trước khi Đồng ý; (B) nút "Lưu thành ý tưởng" ở mỗi tin bản tin. Đã sửa demo + roadmap (2.7, 2.9). Người dùng nói **"chốt"**.

**2.2 đã làm:** Supabase `https://nrvueainkiweuvsoivgp.supabase.co` + Google OAuth (Client ID trong Google Cloud project `harry-ai`, chế độ Testing, Gmail chủ app trong Test users; token có thể hết hạn ~7 ngày → đăng nhập lại). Chủ app = tài khoản đầu tiên đăng nhập, lưu ở bảng `app_owner`; SQL `sql/2.2-chu-app.sql` (đã chạy, gồm GRANT cho `authenticated`). **Mọi bảng dữ liệu sau này: bật RLS, policy dùng `public.la_chu_app()`, và nhớ GRANT cho `authenticated`** (Supabase mới không tự cấp). Config công khai ở `config.js` (sw.js cache v3). Bằng chứng: `docs/bang-chung/2.2/nguoi-la-bi-chan.txt`. Trang đăng nhập hiện ở `index.html` (supabase-js qua CDN).

## Vừa xong
- **2.5b Thông báo đẩy Web Push (XONG, người dùng đã nhận thông báo thật trên iPhone và chốt 2026-11-26; secrets/SQL/deploy đã làm):** người dùng chốt thêm push từ app và GIỮ Telegram (gửi song song). Đã làm: `tools/sinh_vapid.py` (khoá VAPID nằm ở `.env` gốc dự án, đã gitignore; khoá công khai ở `config.js`); `sql/2.5d-push.sql` (bảng `push_dang_ky`, RLS `la_chu_app()`, GRANT authenticated + service_role); `sw.js` v14 (sự kiện `push`, `notificationclick`); hộp "Thông báo trên điện thoại" ở Cài đặt (chưa hỗ trợ / chưa bật / đã bật / bị chặn; Bật, Tắt, Gửi thử); `nhac-viec` dùng `npm:web-push@3.6.7`, gửi push tới mọi đăng ký, 404/410 → xoá đăng ký chết, lỗi push không chặn Telegram/chống trùng (dùng chung `nhac_da_gui`: một trong hai kênh đến nơi là tính đã nhắc), thêm chế độ "Gửi thử" (token đăng nhập + `la_chu_app()`, chỉ push). Kiểm: `tools/thu_push_gia.py` (14 ĐẠT), `tools/thu_thongbao_gia.py` (15 ĐẠT), 3 bộ cũ + `thu_nhac_gia.py` vẫn ĐẠT; bằng chứng `docs/bang-chung/2.5b/`. Đã kiểm chứng thật: `npm:web-push` chạy trên Supabase, iPhone nhận push (nút Gửi thử). Chưa thử nhắc thật theo giờ. (đã làm) chạy SQL 2.5d, thêm 3 secrets VAPID (giá trị ở `F:\Apps\harry-ai\.env`), deploy lại `nhac-viec`, bật trong app iPhone, Gửi thử (xem hướng dẫn).
- **2.6 (code xong, nghiệm thu giả ĐẠT, chờ thử thật):** bảng `y_tuong` (`sql/2.6-y-tuong.sql`, RLS + GRANT authenticated/service_role + realtime), Kho ý tưởng: bảng 3 cột kéo thả, danh sách, lọc ưu tiên/nhãn, 'để lâu' (>14 ngày tính từ `sua_luc`), thùng rác chung với lịch; điện thoại có thanh menu dưới (Lịch/Ý tưởng/Cài đặt). Chưa làm: sắp xếp thứ tự trong cùng cột. Bằng chứng `docs/bang-chung/2.6/` (+ `nghiem-thu/`), `tools/thu_y_tuong_gia.py` (35 ĐẠT). Chưa thử ngón tay thật trên iPhone, realtime thật. sw.js cache v10.
- **2.5 (XONG, đã nghiệm thu 2026-11-26 — tin Telegram đến đúng giờ):** form sự kiện có ô "Nhắc qua Telegram" (không/đúng giờ/15 phút/1 giờ/tuỳ chỉnh) lưu `su_kien.nhac_phut`; Edge Function `supabase/functions/nhac-viec/index.ts` (bung lặp theo giờ VN, gửi Telegram, chống trùng); `sql/2.5a-cot-nhac.sql` + `2.5b-hen-gio.sql`. Hạ tầng đã bật: function `nhac-viec` (Verify JWT tắt), secrets `TELEGRAM_BOT_TOKEN`/`TELEGRAM_CHAT_ID`/`CRON_KEY`, pg_cron mỗi phút (`sql/2.5a/2.5b/2.5c`; 2.5c = GRANT cho `service_role`, từng gây lỗi permission denied → `docs/loi-da-gap.md`). Bằng chứng giả: `docs/bang-chung/2.5/thu-logic-nhac.txt` (12 kiểm tra ĐẠT, `tools/thu_nhac_gia.py`); 2.4 vẫn ĐẠT. sw.js cache v7.
- **2.4 (XONG, đã nghiệm thu):** kéo thả đổi giờ/ngày trong lịch tuần/ngày (chuột kéo luôn; iPhone nhấn giữ ~0,35s rồi kéo; lưới 15 phút); sự kiện lặp ngày/tuần/tháng + "lặp đến hết ngày" (tuỳ chọn), hiện ký hiệu ↻; sửa/xoá/kéo sự kiện lặp hỏi 3 lựa chọn (chỉ này / này và sau / tất cả); thùng rác 30 ngày (khôi phục, xoá hẳn, tự dọn khi mở app; mở từ menu trái hoặc ⚙ Cài đặt). Cách lưu lặp: cột `lap`, `lap_den`, `lap_ngoai` (các lần bị bỏ) trên `su_kien`; "chỉ lần này" = thêm ngoại lệ + tạo sự kiện lẻ mới; "này và sau" = cắt `lap_den` + tạo chuỗi mới. Xoá "chỉ lần này"/"này và sau" cũng tạo bản sao trong thùng rác (khôi phục được). sw.js giờ fetch `no-cache` (cache v6) vì GitHub Pages giữ trang 10 phút → sau mỗi lần đẩy code, đợi ~2 phút rồi Ctrl+Shift+R / đóng mở app. Chưa làm: kéo thả ở lịch tháng, kéo đổi độ dài (có thể thêm nếu người dùng muốn). Bằng chứng: `docs/bang-chung/2.4/` + `tools/thu_lap_gia.py` (Supabase giả nhớ trong bộ nhớ, 17 kiểm tra đều ĐẠT). sw.js cache v5.
- Bước A: thu yêu cầu. Bước B: tạo `CLAUDE.md`, `docs/yeu-cau.md`, `.env.example`, `.gitignore` (thư mục `.claude/rules` bị chặn quyền ghi → quy tắc bảo mật nằm trong `CLAUDE.md`).
- Bước C: 2 vòng phỏng vấn + câu hỏi về lượt Gemini; người dùng nói **"chốt"**.

## Đã quyết định (chọn gì — vì sao — bỏ gì)
- Lưu trữ: GitHub (code, Pages) + Supabase (dữ liệu, đăng nhập Google, đồng bộ tức thì) — an toàn, miễn phí — bỏ "chỉ dùng GitHub lưu dữ liệu" (ghi đè, lộ dữ liệu, phải để token trên điện thoại).
- Chi phí 0 đồng. Chỉ 1 người dùng, đăng nhập Google.
- Nhắc việc đúng giờ (≤ ~1 phút) bằng hẹn giờ của Supabase — bỏ GitHub Actions cho nhắc việc vì trễ 5–15 phút. Bản tin 8:00 có thể dùng GitHub Actions hoặc Supabase (chọn ở Bước D, ưu tiên gom về Supabase cho đơn giản).
- Bản tin 8:00 qua Telegram + trong app; 7 chủ đề; 10–15 tin; 9 báo; chỉ dịch+tóm tắt, gộp trùng; phần đầu: lịch hôm nay, trễ hạn, ý tưởng để lâu.
- Gemini dùng chung khoá với việc Douyin → gộp bản tin 1–2 lần gọi/ngày, model nhẹ (Flash/Flash-Lite); hết lượt → tin nước ngoài để nguyên tiếng Anh (người dùng đồng ý); dự phòng: khoá Gemini riêng.
- Lịch: ngày/tuần/tháng, kéo thả, lặp lại (sửa hỏi 3 lựa chọn như Google Calendar), 5 loại màu mặc định, nhắc qua Telegram, thùng rác 30 ngày.
- Kho ý tưởng: tiêu đề, ghi chú, trạng thái 3 mức, ưu tiên 3 mức, nhãn, hạn (tuỳ chọn); bảng kéo thả 3 cột + danh sách; "để lâu" = Chưa làm > 14 ngày, nhắc tối đa 3/sáng.
- Trợ lý gõ câu tự nhiên → tạo sự kiện/ý tưởng (Gemini).
- Mất mạng: xem được dữ liệu đã tải, thêm/sửa cần mạng.
- Điện thoại iPhone (iOS, đổi từ Android ngày 2026-11-26 — PWA phải mở bằng Safari; khi làm 2.2 phải thử đăng nhập Google trong app đã cài vì iOS hay lỗi; nhắc việc dùng Telegram nên không cần push iOS); giao diện nền sáng kiểu Google Calendar; PWA.
- Để sau: đồng bộ Google Calendar; quản lý video affiliate.
- Thứ tự làm: Lịch → Kho ý tưởng → Bản tin sáng → (sau) công việc affiliate.

## Chưa chắc chắn
- Giới hạn gói miễn phí Gemini/Supabase cụ thể — kiểm chứng khi code (dự kiến đủ cho 1 người).
- Một số báo (Báo Chính phủ, VOV, NHK) có còn RSS không — kiểm chứng ở giai đoạn bản tin.
- Giả định: kho GitHub công khai (để Pages miễn phí); dữ liệu riêng chỉ nằm ở Supabase.
- Người dùng chưa có tài khoản Supabase? (hỏi khi bắt đầu code; hướng dẫn tạo).

## Bước tiếp theo
**2.7 Trợ lý gõ câu tự nhiên** theo `docs/roadmap.md` (ô gõ câu → Gemini model nhẹ → bản xem trước sửa được → Đồng ý mới lưu; khoá `GEMINI_API_KEY` phải để ở Supabase Secrets cho Edge Function, KHÔNG để trong code công khai). Mẫu giao diện: nút ✨ Trợ lý trong `demo/index.html`. Mỗi file SQL/function người dùng dán qua link raw GitHub. Ghi vào 'Agent cố vấn đã quyết' mọi lựa chọn kỹ thuật.

## File đọc đầu tiên
`CLAUDE.md` → `docs/tien-do.md` → `docs/roadmap.md` → `demo/index.html` (mẫu giao diện) → `docs/yeu-cau.md` khi cần chi tiết.

## Lỗi đang gặp
Chưa có.

## Quy ước làm việc với người dùng
Khi bảo người dùng mở file/trang nào, **luôn kèm link bấm được** (file trong kho: `https://raw.githubusercontent.com/ducthaiktcn02/harry-ai/main/<đường dẫn>`). Mỗi file SQL chỉ chứa việc dán nguyên được.
