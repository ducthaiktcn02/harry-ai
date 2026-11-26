# Nguồn tin chốt cho bản tin sáng (2.8)

Kiểm thật ngày 2026-11-26 bằng `py -3.12 tools/kiem_rss.py` (chi tiết từng URL: `kiem-rss.txt`). Cấu hình dùng thật nằm ở `supabase/functions/ban-tin-lay/nguon.ts`.

## Báo nào còn RSS
| Báo | Kết quả | Ghi chú |
|---|---|---|
| VnExpress | CÒN | 6 mục dùng |
| Tuổi Trẻ | CÒN | 6 mục dùng |
| Thanh Niên | CÒN | 6 mục dùng (`cong-nghe-game.rss` chết, đã thay bằng `cong-nghe.rss`) |
| VOV | CÒN, nhưng ĐƯỜNG DẪN ĐÃ ĐỔI | Dạng cũ có số (`chinh-tri-212.rss`, `kinh-te-3.rss`…) trả 404. Dạng mới không số, lấy từ https://vov.vn/rss.html. `doanh-nghiep.rss` có trong danh sách của VOV nhưng thực tế 404. |
| Báo Chính phủ | CÒN, đường dẫn kiểu `baochinhphu.vn/<mục>.rss` | Dạng `/rss/<mục>.rss` và `home.rss` 404. Không có mục Thế giới. |
| BBC | CÒN | 5 mục |
| The Guardian | CÒN | 5 mục |
| DW | CÒN một phần | Chỉ `rss-en-world` và `rss-en-bus`; `rss-en-sci`, `rss-en-sport` trả trang web (không phải XML) nên bỏ |
| **NHK World** | **BỎ — không còn RSS** | Mọi đường dẫn tiếng Anh `/nhkworld/en/news/feeds/*` trả 404 (trang `/en/news/` chuyển hướng sang `/nhkworld/news/`, không có RSS). Còn `www3.nhk.or.jp/rss/news/cat*.xml` nhưng là tiếng Nhật và ngừng cập nhật từ 08/2026; `data/en/news/all.json` không phải RSS và cũng cũ (09/2026). |

## Bảng nguồn chốt (báo → chủ đề → URL)
Thời sự trong nước
- VnExpress: https://vnexpress.net/rss/thoi-su.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/thoi-su.rss
- Thanh Niên: https://thanhnien.vn/rss/thoi-su.rss
- VOV: https://vov.vn/rss/chinh-tri.rss · https://vov.vn/rss/xa-hoi.rss
- Báo Chính phủ: https://baochinhphu.vn/chinh-tri.rss · https://baochinhphu.vn/thoi-su.rss

Thế giới
- VnExpress: https://vnexpress.net/rss/the-gioi.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/the-gioi.rss
- Thanh Niên: https://thanhnien.vn/rss/the-gioi.rss
- VOV: https://vov.vn/rss/the-gioi.rss
- BBC: https://feeds.bbci.co.uk/news/world/rss.xml
- The Guardian: https://www.theguardian.com/world/rss
- DW: https://rss.dw.com/xml/rss-en-world

Kinh tế – tài chính (đồng thời là nguồn của Kinh doanh online / TMĐT, xem bên dưới)
- VnExpress: https://vnexpress.net/rss/kinh-doanh.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/kinh-doanh.rss
- Thanh Niên: https://thanhnien.vn/rss/kinh-te.rss
- VOV: https://vov.vn/rss/kinh-te.rss
- Báo Chính phủ: https://baochinhphu.vn/kinh-te.rss
- BBC: https://feeds.bbci.co.uk/news/business/rss.xml
- The Guardian: https://www.theguardian.com/business/rss
- DW: https://rss.dw.com/xml/rss-en-bus

Công nghệ – AI
- VnExpress: https://vnexpress.net/rss/so-hoa.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/nhip-song-so.rss
- Thanh Niên: https://thanhnien.vn/rss/cong-nghe.rss
- VOV: https://vov.vn/rss/cong-nghe.rss
- Báo Chính phủ: https://baochinhphu.vn/khoa-hoc-cong-nghe.rss
- BBC: https://feeds.bbci.co.uk/news/technology/rss.xml
- The Guardian: https://www.theguardian.com/technology/rss

Kinh doanh online / TMĐT
- Không báo nào có RSS riêng cho mục này. Cách làm: lấy từ các RSS Kinh tế ở trên, tin nào có từ khoá (thương mại điện tử, Shopee, Lazada, TikTok, Temu, livestream bán hàng, e-commerce…) thì xếp vào chủ đề này (danh sách từ khoá: `TMDT_TU_KHOA` trong `nguon.ts`). Ngày chạy thử chỉ ra 2 tin → chủ đề này thường mỏng; 2.9 có thể dùng tin Kinh tế thay khi thiếu.

Sức khoẻ
- VnExpress: https://vnexpress.net/rss/suc-khoe.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/suc-khoe.rss
- Thanh Niên: https://thanhnien.vn/rss/suc-khoe.rss
- VOV: https://vov.vn/rss/suc-khoe.rss
- Báo Chính phủ: https://baochinhphu.vn/y-te.rss
- BBC: https://feeds.bbci.co.uk/news/health/rss.xml
- The Guardian: https://www.theguardian.com/society/health/rss

Thể thao
- VnExpress: https://vnexpress.net/rss/the-thao.rss
- Tuổi Trẻ: https://tuoitre.vn/rss/the-thao.rss
- Thanh Niên: https://thanhnien.vn/rss/the-thao.rss
- VOV: https://vov.vn/rss/the-thao.rss
- BBC: https://feeds.bbci.co.uk/sport/rss.xml
- The Guardian: https://www.theguardian.com/sport/rss

Tổng: 42 RSS của 8 báo (bỏ NHK World).

## Điểm cần nhớ về dữ liệu
- Tuổi Trẻ và Báo Chính phủ ghi giờ dạng `11/26/2026 7:23:00 PM` (giờ Việt Nam, không có múi giờ) — code đã xử lý.
- Báo Chính phủ không có mục Thế giới; DW/BBC/Guardian/… là tiếng Anh (2.9 mới dịch).
- Gộp trùng: cùng link (bỏ utm/fbclid/#/www) hoặc tiêu đề giống ≥ 60% từ (sau bỏ dấu). Không gộp được tin cùng sự kiện khác ngôn ngữ (VN với Anh).
