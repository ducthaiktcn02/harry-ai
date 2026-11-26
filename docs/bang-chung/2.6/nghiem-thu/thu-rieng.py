import sys, json, os, time
src = open(r'F:\Apps\harry-ai\tools\thu_y_tuong_gia.py', encoding='utf-8').read().split('ok_all = True')[0]
OUTDIR = r'F:\Apps\harry-ai\docs\bang-chung\2.6\nghiem-thu'
sys.argv = ['x', OUTDIR]
g = {'__file__': r'F:\Apps\harry-ai\tools\thu_y_tuong_gia.py'}
exec(src, g)
ROOT = g['ROOT']; YT0 = g['YT']
from playwright.sync_api import sync_playwright
res = []
def chk(n, c): res.append((n, bool(c))); print('ĐẠT ' if c else 'TRƯỢT', n)
def mk(yt):
    f = g['FAKE']; a = json.dumps(YT0)
    assert a in f
    return f.replace(a, json.dumps(yt), 1)
def open_(b, yt, **kw):
    ctx = b.new_context(**kw); pg = ctx.new_page(); errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    alerts = []
    pg.on('dialog', lambda d: (alerts.append(d.message), d.accept()))
    body = mk(yt)
    pg.route('**/@supabase/supabase-js@2', lambda r: r.fulfill(body=body, content_type='application/javascript'))
    pg.goto('file:///' + ROOT.replace('\\', '/') + '/index.html'); pg.wait_for_selector('#app:not([hidden])')
    pg.click('#duoi a[data-p=y]' if kw.get('is_mobile') else '.nav a[data-p=y]'); pg.wait_for_timeout(300)
    pg.__e = errs; return ctx, pg, errs, alerts
def Y(i, t, tt='chua_lam', uu='vua', nhan=None, ghi=None):
    return dict(id=i, tieu_de=t, ghi_chu=ghi, trang_thai=tt, uu_tien=uu, nhan=nhan or [], han=None, thu_tu=int(str(i).lstrip('y')), tao_luc='2026-11-25T00:00:00+00:00', sua_luc='2026-11-25T00:00:00+00:00', xoa_luc=None, nguon=None, link=None)
X = '<img src=x onerror=alert(1)>'
P = lambda n: OUTDIR + '\\' + n
with sync_playwright() as p:
    b = p.chromium.launch(channel='chrome')
    ctx, pg, errs, al = open_(b, [], viewport=dict(width=1200, height=800))
    print(errs); chk('Rỗng: 3 cột, 0 thẻ, không lỗi JS', pg.locator('.lane').count() == 3 and pg.locator('.card').count() == 0 and not errs)
    pg.screenshot(path=P('a1-rong-bang.png'))
    pg.click('#bDs'); pg.wait_for_timeout(200)
    chk('Rỗng: danh sách hiện thông báo trống', pg.locator('text=Chưa có ý tưởng nào khớp').count() == 1)
    pg.screenshot(path=P('a2-rong-ds.png')); pg.click('#bBang')
    pg.click('#bYMoi'); pg.fill('#yTen', '   '); pg.click('#yLuu'); pg.wait_for_timeout(200)
    chk('Tiêu đề toàn khoảng trắng: không lưu, hộp thoại còn mở', len(pg.evaluate('window.__DB.y_tuong')) == 0 and pg.locator('#yTen').count() == 1)
    pg.fill('#yTen', X); pg.fill('#yGhi', X)
    pg.fill('#yNhan', X + ', "><script>alert(2)</script>, a&b, \' onmouseover=alert(3)')
    pg.click('#yLuu'); pg.wait_for_timeout(400)
    chk('XSS: không có alert nào bật', not al)
    chk('XSS: không có img/script bị chèn', pg.locator('#yView img, #yView script, #toast img').count() == 0)
    chk('XSS: tiêu đề hiện thành chữ', pg.locator('.card .t').first.inner_text() == X)
    chk('XSS: ghi chú hiện thành chữ', pg.locator('.card .n').first.inner_text() == X)
    tg = pg.locator('.card .tags').first.inner_text()
    chk('XSS: nhãn đặc biệt hiện nguyên chữ', 'a&b' in tg and '<script>' in tg)
    pg.screenshot(path=P('a3-xss-bang.png'))
    pg.locator('.card').first.click(); pg.wait_for_timeout(200)
    chk('XSS: mở sửa, ô tiêu đề giữ nguyên chuỗi', pg.input_value('#yTen') == X and pg.locator('#dlg img').count() == 0)
    chk('XSS: ô nhãn giữ nguyên (không vỡ thuộc tính value)', 'onmouseover=alert(3)' in pg.input_value('#yNhan') and pg.locator('#yNhan[onmouseover]').count() == 0)
    pg.click('#yHuy'); pg.click('#bDs'); pg.wait_for_timeout(200)
    chk('XSS: danh sách không chèn thẻ', pg.locator('#yView img, #yView script').count() == 0)
    opts = pg.locator('#fNhan option').all_inner_texts()
    chk('XSS: bộ lọc nhãn liệt kê nhãn đặc biệt đúng chữ', any('<script>' in o for o in opts))
    pg.select_option('#fNhan', label=[o for o in opts if 'a&b' in o][0]); pg.wait_for_timeout(200)
    chk('Lọc theo nhãn a&b: 1 dòng', pg.locator('.dong').count() == 1)
    pg.screenshot(path=P('a4-xss-ds-loc.png'))
    pg.select_option('#fNhan', ''); pg.locator('.dong').first.click(); pg.click('#yXoa'); pg.wait_for_timeout(400)
    chk('XSS: sau xoá vẫn không alert', not any(m == '1' for m in al))
    print('   (hộp confirm đã thấy:', [m[:40] for m in al], ')')
    if pg.locator('.nav a[data-p=rac]').count(): pg.click('.nav a[data-p=rac]')
    pg.wait_for_timeout(300); pg.screenshot(path=P('a5-xss-rac.png'))
    chk('XSS thùng rác: không chèn thẻ, có mục đã xoá', pg.locator('#dsRac img, #dsRac script').count() == 0 and 'img src' in pg.locator('#dsRac').inner_text())
    chk('Không lỗi JS suốt loạt rỗng/XSS', not errs)
    ctx.close()

    yt = [Y('y%d' % i, f'Ý tưởng số {i} ' + ('dài ' * (i % 7)), ['chua_lam', 'dang_lam', 'xong'][i % 3], ['cao', 'vua', 'thap'][i % 3], [f'n{i % 5}', 'chung']) for i in range(1, 151)]
    t = time.time(); ctx, pg, errs, al = open_(b, yt, viewport=dict(width=1200, height=800)); dt = time.time() - t
    print(errs, pg.locator('.card').count()); chk(f'150 ý tưởng: đủ 150 thẻ (mở {dt:.1f}s)', pg.locator('.card').count() == 150 and not errs)
    pg.screenshot(path=P('b1-150-bang.png'), full_page=True)
    pg.select_option('#fNhan', 'n2'); pg.wait_for_timeout(200)
    chk('150: lọc nhãn n2 = 30 thẻ', pg.locator('.card').count() == 30)
    pg.select_option('#fNhan', ''); pg.click('#bDs'); pg.wait_for_timeout(300)
    chk('150: danh sách 150 dòng', pg.locator('.dong').count() == 150)
    pg.screenshot(path=P('b2-150-ds.png'))
    pg.click('#bBang'); pg.wait_for_timeout(200)
    c = pg.locator('.lane[data-s=chua_lam] .card').nth(40); c.scroll_into_view_if_needed()
    bb = c.bounding_box(); lb = pg.locator('.lane[data-s=xong]').bounding_box()
    tid = c.get_attribute('data-yid')
    pg.mouse.move(bb['x'] + 20, bb['y'] + 10); pg.mouse.down(); pg.mouse.move(bb['x'] + 40, bb['y'] + 30, steps=4)
    vp = pg.viewport_size
    pg.mouse.move(lb['x'] + lb['width'] / 2, min(max(lb['y'], 10) + 60, vp['height'] - 20), steps=8); pg.mouse.up(); pg.wait_for_timeout(400)
    print('   id', tid, 'trạng thái sau kéo', pg.evaluate("i=>window.__DB.y_tuong.find(r=>String(r.id)==i).trang_thai", tid))
    chk('150: kéo thẻ sâu trong cột dài sang Đã xong', pg.evaluate("i=>window.__DB.y_tuong.find(r=>String(r.id)==i).trang_thai", tid) == 'xong')
    ctx.close()

    ctx, pg, errs, al = open_(b, yt[:40] + [Y('y999', X + ' ' + 'x' * 80, nhan=['nhan-rat-dai-' + 'z' * 60, X])], viewport=dict(width=390, height=800), has_touch=True, is_mobile=True)
    sw = pg.evaluate('[document.documentElement.scrollWidth, innerWidth]')
    chk(f'390px bảng: không tràn ngang trang {sw}', sw[0] <= sw[1])
    pg.screenshot(path=P('c1-dt-bang.png'))
    pg.click('#bDs'); pg.wait_for_timeout(300)
    sw = pg.evaluate('[document.documentElement.scrollWidth, innerWidth]')
    chk(f'390px danh sách: không tràn ngang {sw}', sw[0] <= sw[1])
    pg.screenshot(path=P('c2-dt-ds.png'))
    pg.click('#bBang'); pg.click('#bYMoi'); pg.wait_for_timeout(300)
    r = pg.evaluate("(()=>{const b=document.querySelector('#dlg').getBoundingClientRect();return [b.left,b.right,b.top,b.bottom,innerWidth,innerHeight]})()")
    chk(f'390px hộp thoại trong màn hình {r}', r[0] >= 0 and r[1] <= r[4] + 1)
    chk('390px nút Lưu thấy được', pg.locator('#yLuu').is_visible() and pg.evaluate("(()=>{const b=document.querySelector('#yLuu').getBoundingClientRect();return b.bottom<=innerHeight+1&&b.right<=innerWidth})()"))
    pg.screenshot(path=P('c3-dt-hop-thoai.png'))
    chk('Không lỗi JS (điện thoại)', not errs)
    ctx.close()
print('TRƯỢT:', [n for n, c in res if not c])
