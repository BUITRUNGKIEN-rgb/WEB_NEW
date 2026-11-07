"""Read-only check before a GitHub push: never deletes or edits local files."""
from __future__ import annotations
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
FORBIDDEN_PREFIX=('data/','model/','results/','results_cnn/','backup_ui/','backup_before_','logs/','.venv/','venv/','env/','.vscode/','.idea/')
ALLOWED_PLACEHOLDERS={'data/README.txt','model/README.txt','results/README.txt','results_cnn/README.txt'}
FORBIDDEN_EXT={'.pth','.pt','.pkl','.joblib','.ckpt','.onnx','.safetensors','.h5','.hdf5','.csv','.parquet','.npy','.npz','.zip','.7z','.rar','.pem','.key','.p12','.pfx'}
FORBIDDEN_NAMES={'.env','.streamlit/secrets.toml','secrets.toml','credentials.json'}
MAX_FILE_MB=25

def git_list_staged():
    p=subprocess.run(['git','ls-files','--cached','-z'],cwd=ROOT,capture_output=True)
    if p.returncode:
        return None
    return [x.decode('utf-8',errors='replace').replace('\\','/') for x in p.stdout.split(b'\0') if x]

def reason_for(name):
    key=name.replace('\\','/').lower()
    if key in {x.lower() for x in ALLOWED_PLACEHOLDERS}:
        return None
    if key in FORBIDDEN_NAMES or key.startswith('.env.') or key.endswith('/secrets.toml'):
        return 'private config / credentials'
    if key.startswith(FORBIDDEN_PREFIX):
        return 'dataset, trained model or local experiment results'
    if Path(key).suffix in FORBIDDEN_EXT:
        return 'private data, checkpoint or archive file'
    if Path(key).name in ('thumbs.db','.ds_store'):
        return 'OS cache'
    f=ROOT/name
    try:
        if f.is_file() and f.stat().st_size > MAX_FILE_MB*1024*1024:
            return f'file is larger than {MAX_FILE_MB} MB'
    except OSError:
        return 'file cannot be inspected'
    return None

def main():
    staged=git_list_staged()
    if staged is None:
        print('[WARN] Repository chua git init / chua co git. Script chi kiem tra goi mau, khong xac minh git staged.')
        staged=[str(p.relative_to(ROOT)).replace('\\','/') for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts]
    elif not staged:
        print('[WARN] Chua git add . : hien khong co file nao duoc theo doi trong Git index.')
        return 2
    bad=[(name,reason_for(name)) for name in staged if reason_for(name)]
    print(f'[INFO] Da kiem tra {len(staged)} file.')
    if bad:
        for name,why in bad: print(f'[BLOCK] {name}  --> {why}')
        print('[BLOCK] KHONG GIT PUSH truoc khi loai bo cac file nhay cam khoi Git index.')
        return 1
    print('[OK] Khong phat hien dataset, checkpoint, ket qua hay file bi mat trong danh sach duoc kiem tra.')
    print('[NOTE] Script khong the cam ket 100% khong co secrets nam trong file code; hay tu ra soat noi dung.')
    return 0

if __name__=='__main__':
    sys.exit(main())
