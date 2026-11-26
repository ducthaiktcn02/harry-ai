"""Sinh cặp khoá VAPID (Web Push) và ghi vào .env ở gốc dự án. KHÔNG in khoá riêng ra màn hình.
Chạy: py -3.12 tools/sinh_vapid.py   (nếu .env đã có VAPID_PRIVATE_KEY thì không ghi đè, trừ khi thêm --moi)
In ra chỉ khoá CÔNG KHAI (dán vào config.js)."""
import os, sys, base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ENV = os.path.join(ROOT, '.env')
b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b'=').decode()
cur = open(ENV, encoding='utf-8').read() if os.path.exists(ENV) else ''
if 'VAPID_PRIVATE_KEY=' in cur and '--moi' not in sys.argv:
    print('Đã có khoá trong .env, giữ nguyên.')
    print('VAPID_PUBLIC_KEY =', [l.split('=', 1)[1] for l in cur.splitlines() if l.startswith('VAPID_PUBLIC_KEY=')][0]); sys.exit(0)
k = ec.generate_private_key(ec.SECP256R1())
priv = b64(k.private_numbers().private_value.to_bytes(32, 'big'))
pub = b64(k.public_key().public_bytes(serialization.Encoding.X962, serialization.PublicFormat.UncompressedPoint))
keep = ''.join(l + '\n' for l in cur.splitlines() if not l.startswith('VAPID_'))
open(ENV, 'w', encoding='utf-8').write(keep + f'VAPID_PUBLIC_KEY={pub}\nVAPID_PRIVATE_KEY={priv}\nVAPID_SUBJECT=mailto:harry-ai@users.noreply.github.com\n')
print('Đã ghi .env. VAPID_PUBLIC_KEY =', pub)
