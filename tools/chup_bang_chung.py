"""Chụp ảnh trang đã đăng (khổ điện thoại) + kiểm tra điều kiện cài PWA."""
import os
import sys
from playwright.sync_api import sync_playwright

URL = "https://ducthaiktcn02.github.io/harry-ai/"
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)

with sync_playwright() as p:
    b = p.chromium.launch(channel="chrome")
    ctx = b.new_context(viewport={"width": 390, "height": 760}, device_scale_factor=2, is_mobile=True)
    page = ctx.new_page()
    page.goto(URL, wait_until="networkidle")
    page.wait_for_function("document.getElementById('trangthai').textContent.length>0", timeout=10000)
    page.screenshot(path=os.path.join(OUT, "trang-dien-thoai.png"))
    m = page.evaluate("fetch('manifest.webmanifest').then(r=>r.json())")
    reg = page.evaluate("navigator.serviceWorker.ready.then(r=>r.active.state)")
    print("ten:", m["name"], "| display:", m["display"], "| icons:", len(m["icons"]))
    print("service worker:", reg)
    print("tieu de:", page.title())
    b.close()
