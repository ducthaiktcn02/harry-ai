"""Tạo icon PNG (nền xanh, chữ H trắng) bằng thư viện chuẩn của Python."""
import os
import struct
import zlib


def png(size):
    blue = (26, 115, 232)
    white = (255, 255, 255)
    s = size
    # chữ H: 2 cột dọc + thanh ngang, nằm trong vùng an toàn ở giữa
    x0, x1 = int(s * 0.30), int(s * 0.70)
    y0, y1 = int(s * 0.28), int(s * 0.72)
    w = max(2, int(s * 0.10))
    rows = []
    for y in range(s):
        row = bytearray([0])
        for x in range(s):
            on = False
            if y0 <= y <= y1:
                if x0 <= x < x0 + w or x1 - w < x <= x1:
                    on = True
                if abs(y - s // 2) < w // 2 + 1 and x0 <= x <= x1:
                    on = True
            row += bytes(white if on else blue)
        rows.append(bytes(row))
    raw = b"".join(rows)

    def chunk(t, d):
        c = struct.pack(">I", len(d)) + t + d
        return c + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", s, s, 8, 2, 0, 0, 0)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw, 9)) + chunk(b"IEND", b"")


out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "icons")
os.makedirs(out, exist_ok=True)
for n in (192, 512):
    with open(os.path.join(out, f"icon-{n}.png"), "wb") as f:
        f.write(png(n))
print("ok")
