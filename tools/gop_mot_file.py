# Gộp mỗi Edge Function nhiều file thành 1 file để dán vào trình soạn thảo web Supabase
# (trình soạn thảo web hay không giữ file thứ hai -> lỗi "Module not found").
# Chạy: py -3.12 tools/gop_mot_file.py   -> ra supabase/dan-mot-file/*.ts
import re, pathlib
G = pathlib.Path(__file__).resolve().parent.parent
B = G / 'supabase' / 'functions'
O = G / 'supabase' / 'dan-mot-file'
O.mkdir(exist_ok=True)

def doc(p):
    return p.read_text(encoding='utf-8')

def bo_import_noi_bo(s):
    return re.sub(r"^import\s[^;]*?from\s+'\./[^']+';[ \t]*\r?\n", '', s, flags=re.M)

def gop(ten, files):
    dau = f"// BẢN GỘP 1 FILE của {ten} ({' + '.join(files)}), dán vào index.ts trên web Supabase.\n// Đừng sửa tay: sinh bằng tools/gop_mot_file.py\n"
    nd = dau + '\n'.join(bo_import_noi_bo(doc(B / ten / f)) for f in files)
    (O / f'{ten}.ts').write_text(nd.replace('\r\n', '\n'), encoding='utf-8', newline='\n')

gop('ban-tin-lay', ['nguon.ts', 'loi.ts', 'index.ts'])
gop('ban-tin-gui', ['loi.ts', 'index.ts'])
print('xong')
