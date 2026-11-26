"""Chạy bộ kiểm ban-tin-lay bằng RSS giả (tools/mau_rss/) qua Deno. Ghi log vào docs/bang-chung/2.8/test-ban-tin-gia.txt
Chạy: py -3.12 tools/thu_ban_tin_gia.py
"""
import glob, json, os, shutil, subprocess, sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
goc = Path(__file__).resolve().parent.parent
deno = shutil.which('deno')
if not deno:
    c = glob.glob(os.path.expandvars(r'%LOCALAPPDATA%\Microsoft\WinGet\Packages\DenoLand.Deno*\deno.exe'))
    deno = c[0] if c else None
if not deno:
    sys.exit('Chưa có deno. Cài: winget install DenoLand.Deno')
p = subprocess.run([deno, 'run', '--allow-read', str(goc / 'tools' / 'thu_ban_tin_gia.ts')], capture_output=True, text=True, encoding='utf-8')
if p.returncode != 0:
    print(p.stdout, p.stderr)
    sys.exit('Deno báo lỗi khi chạy test')
kq = json.loads(p.stdout.strip().splitlines()[-1])
dong = [f'[{"ĐẠT" if k["dat"] else "TRƯỢT"}] {k["ten"]}' + ('' if k['dat'] or not k['chi_tiet'] else f'\n        -> {k["chi_tiet"]}') for k in kq]
ver = subprocess.run([deno, '--version'], capture_output=True, text=True).stdout.splitlines()[0]
out = '\n'.join(dong) + f'\n\n{sum(k["dat"] for k in kq)}/{len(kq)} ĐẠT ({ver})\n'
d = goc / 'docs' / 'bang-chung' / '2.8'
d.mkdir(parents=True, exist_ok=True)
(d / 'test-ban-tin-gia.txt').write_text(out, encoding='utf-8')
print(out)
sys.exit(0 if all(k['dat'] for k in kq) else 1)
