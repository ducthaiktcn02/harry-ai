"""Kiểm tra RSS ứng viên của 9 báo cho 7 chủ đề (giai đoạn 2.8). Chỉ GET công khai, không khoá.
Chạy: py -3.12 tools/kiem_rss.py   -> ghi docs/bang-chung/2.8/kiem-rss.txt và kiem-rss.json
"""
import http.client, json, re, sys, time, urllib.request, urllib.error, xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor
from email.utils import parsedate_to_datetime
from datetime import datetime, timedelta, timezone
from pathlib import Path

UA = 'Mozilla/5.0 (compatible; HarryAI-RSS-check/1.0)'
CD = ['Thời sự trong nước', 'Thế giới', 'Kinh tế – tài chính', 'Công nghệ – AI', 'Kinh doanh online / TMĐT', 'Sức khoẻ', 'Thể thao']
TS, TG, KT, CN, TM, SK, TT = CD

# (báo, chủ đề, URL ứng viên)
UV = [
    ('VnExpress', TS, 'https://vnexpress.net/rss/thoi-su.rss'),
    ('VnExpress', TG, 'https://vnexpress.net/rss/the-gioi.rss'),
    ('VnExpress', KT, 'https://vnexpress.net/rss/kinh-doanh.rss'),
    ('VnExpress', CN, 'https://vnexpress.net/rss/so-hoa.rss'),
    ('VnExpress', TM, 'https://vnexpress.net/rss/kinh-doanh.rss'),
    ('VnExpress', SK, 'https://vnexpress.net/rss/suc-khoe.rss'),
    ('VnExpress', TT, 'https://vnexpress.net/rss/the-thao.rss'),
    ('Tuổi Trẻ', TS, 'https://tuoitre.vn/rss/thoi-su.rss'),
    ('Tuổi Trẻ', TG, 'https://tuoitre.vn/rss/the-gioi.rss'),
    ('Tuổi Trẻ', KT, 'https://tuoitre.vn/rss/kinh-doanh.rss'),
    ('Tuổi Trẻ', CN, 'https://tuoitre.vn/rss/nhip-song-so.rss'),
    ('Tuổi Trẻ', SK, 'https://tuoitre.vn/rss/suc-khoe.rss'),
    ('Tuổi Trẻ', TT, 'https://tuoitre.vn/rss/the-thao.rss'),
    ('Thanh Niên', TS, 'https://thanhnien.vn/rss/thoi-su.rss'),
    ('Thanh Niên', TG, 'https://thanhnien.vn/rss/the-gioi.rss'),
    ('Thanh Niên', KT, 'https://thanhnien.vn/rss/kinh-te.rss'),
    ('Thanh Niên', CN, 'https://thanhnien.vn/rss/cong-nghe.rss'),
    ('Thanh Niên', CN, 'https://thanhnien.vn/rss/cong-nghe-game.rss'),
    ('Thanh Niên', SK, 'https://thanhnien.vn/rss/suc-khoe.rss'),
    ('Thanh Niên', TT, 'https://thanhnien.vn/rss/the-thao.rss'),
    ('VOV', TS, 'https://vov.vn/rss/chinh-tri.rss'),
    ('VOV', TS, 'https://vov.vn/rss/xa-hoi.rss'),
    ('VOV', TG, 'https://vov.vn/rss/the-gioi.rss'),
    ('VOV', KT, 'https://vov.vn/rss/kinh-te.rss'),
    ('VOV', TM, 'https://vov.vn/rss/doanh-nghiep.rss'),
    ('VOV', CN, 'https://vov.vn/rss/cong-nghe.rss'),
    ('VOV', SK, 'https://vov.vn/rss/suc-khoe.rss'),
    ('VOV', TT, 'https://vov.vn/rss/the-thao.rss'),
    ('VOV', TS, 'https://vov.vn/rss/home.rss'),
    ('VOV', TS, 'https://vov.vn/rss/chinh-tri-212.rss'),
    ('Báo Chính phủ', TS, 'https://baochinhphu.vn/rss/home.rss'),
    ('Báo Chính phủ', TS, 'https://baochinhphu.vn/chinh-tri.rss'),
    ('Báo Chính phủ', TS, 'https://baochinhphu.vn/thoi-su.rss'),
    ('Báo Chính phủ', TS, 'https://baochinhphu.vn/rss/chinh-tri.rss'),
    ('Báo Chính phủ', KT, 'https://baochinhphu.vn/kinh-te.rss'),
    ('Báo Chính phủ', KT, 'https://baochinhphu.vn/rss/kinh-te.rss'),
    ('Báo Chính phủ', TG, 'https://baochinhphu.vn/thoi-su-quoc-te.rss'),
    ('Báo Chính phủ', SK, 'https://baochinhphu.vn/y-te.rss'),
    ('Báo Chính phủ', CN, 'https://baochinhphu.vn/khoa-hoc-cong-nghe.rss'),
    ('BBC', TG, 'https://feeds.bbci.co.uk/news/world/rss.xml'),
    ('BBC', KT, 'https://feeds.bbci.co.uk/news/business/rss.xml'),
    ('BBC', CN, 'https://feeds.bbci.co.uk/news/technology/rss.xml'),
    ('BBC', SK, 'https://feeds.bbci.co.uk/news/health/rss.xml'),
    ('BBC', TT, 'https://feeds.bbci.co.uk/sport/rss.xml'),
    ('The Guardian', TG, 'https://www.theguardian.com/world/rss'),
    ('The Guardian', KT, 'https://www.theguardian.com/business/rss'),
    ('The Guardian', CN, 'https://www.theguardian.com/technology/rss'),
    ('The Guardian', SK, 'https://www.theguardian.com/society/health/rss'),
    ('The Guardian', TT, 'https://www.theguardian.com/sport/rss'),
    ('DW', TG, 'https://rss.dw.com/xml/rss-en-world'),
    ('DW', KT, 'https://rss.dw.com/xml/rss-en-bus'),
    ('DW', CN, 'https://rss.dw.com/xml/rss-en-sci'),
    ('DW', TT, 'https://rss.dw.com/xml/rss-en-sport'),
    ('DW', TG, 'https://rss.dw.com/xml/rss-en-all'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/nhkworld/en/news/feeds/'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/nhkworld/en/news/feeds/world.xml'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/nhkworld/en/news/rss.xml'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/nhkworld/news/feeds/world.xml'),
    ('NHK World', KT, 'https://www3.nhk.or.jp/nhkworld/en/news/feeds/business.xml'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/nhkworld/data/en/news/all.xml'),
    ('NHK World', TG, 'https://www3.nhk.or.jp/rss/news/cat6.xml'),
    ('Tuổi Trẻ', TM, 'https://tuoitre.vn/rss/kinh-doanh.rss'),
    ('Thanh Niên', TM, 'https://thanhnien.vn/rss/kinh-te.rss'),
    ('Báo Chính phủ', TM, 'https://baochinhphu.vn/kinh-te.rss'),
]


def local(tag):
    return tag.rsplit('}', 1)[-1]


def thu(url):
    t0 = time.time()
    r = {'url': url, 'song': False, 'ma': None, 'loi': None, 'so_tin': 0, 'moi_nhat': None, 'tieu_de_moi_nhat': None, 'giay': 0}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA, 'Accept': 'application/rss+xml, application/xml, text/xml, */*'})
        for lan in (1, 2):  # thử tối đa 2 lần (Thanh Niên đôi khi cắt ngang giữa chừng)
            try:
                with urllib.request.urlopen(req, timeout=12) as f:
                    r['ma'] = f.status
                    raw = f.read()
                break
            except (http.client.IncompleteRead, ConnectionError, TimeoutError):
                if lan == 2:
                    raise
        try:
            root = ET.fromstring(raw)
        except ET.ParseError as e:
            r['loi'] = 'Không phải XML hợp lệ (có thể là trang HTML): ' + str(e)[:60]
            return r
        items = [e for e in root.iter() if local(e.tag) in ('item', 'entry')]
        best = None
        for it in items:
            d = {local(c.tag): (c.text or '').strip() for c in it}
            raw_t = d.get('pubDate') or d.get('published') or d.get('updated') or d.get('date') or ''
            dt = None
            try:
                dt = parsedate_to_datetime(raw_t)
            except Exception:
                try:
                    dt = datetime.fromisoformat(raw_t.replace('Z', '+00:00'))
                except Exception:
                    try:  # Tuổi Trẻ, Báo Chính phủ: '11/26/2026 7:23:00 PM' (giờ Việt Nam)
                        dt = datetime.strptime(raw_t, '%m/%d/%Y %I:%M:%S %p').replace(tzinfo=timezone(timedelta(hours=7)))
                    except Exception:
                        pass
            if dt is not None:
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if best is None or dt > best[0]:
                    best = (dt, d.get('title', ''))
        r['so_tin'] = len(items)
        if best:
            r['moi_nhat'] = best[0].astimezone(timezone.utc).strftime('%Y-%m-%d %H:%MZ')
            r['tieu_de_moi_nhat'] = best[1][:90]
        r['song'] = len(items) > 0
        if not items:
            r['loi'] = 'XML hợp lệ nhưng không có tin'
    except urllib.error.HTTPError as e:
        r['ma'] = e.code; r['loi'] = f'HTTP {e.code}'
    except Exception as e:
        r['loi'] = type(e).__name__ + ': ' + str(e)[:80]
    r['giay'] = round(time.time() - t0, 1)
    return r


def main():
    out_dir = Path(__file__).resolve().parent.parent / 'docs' / 'bang-chung' / '2.8'
    out_dir.mkdir(parents=True, exist_ok=True)
    urls = sorted({u for _, _, u in UV})
    with ThreadPoolExecutor(8) as ex:
        kq = dict(zip(urls, ex.map(thu, urls)))
    lines = [f'Kiểm RSS lúc {datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M")}Z — {len(urls)} URL ứng viên', '']
    res = []
    for bao, cd, u in UV:
        r = kq[u]
        tt = 'SỐNG ' if r['song'] else 'CHẾT '
        lines.append(f'[{tt}] {bao} | {cd}\n   {u}\n   mã={r["ma"]} tin={r["so_tin"]} mới nhất={r["moi_nhat"]} ({r["giay"]}s) {r["loi"] or ""}\n   «{r["tieu_de_moi_nhat"] or ""}»')
        res.append({'bao': bao, 'chu_de': cd, **r})
    lines.append('')
    lines.append('TÓM TẮT THEO BÁO (số URL sống / tổng):')
    for bao in dict.fromkeys(b for b, _, _ in UV):
        rs = [x for x in res if x['bao'] == bao]
        lines.append(f'  {bao}: {sum(1 for x in rs if x["song"])}/{len(rs)}')
    (out_dir / 'kiem-rss.txt').write_text('\n'.join(lines) + '\n', encoding='utf-8')
    (out_dir / 'kiem-rss.json').write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding='utf-8')
    print('\n'.join(lines[-12:]))


if __name__ == '__main__':
    main()
