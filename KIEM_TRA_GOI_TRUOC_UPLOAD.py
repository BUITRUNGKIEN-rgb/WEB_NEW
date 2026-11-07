"""Kiem tra read-only bo ma AI02 V14 truoc khi tai len GitHub."""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parent
REQUIRED=('index.html','.nojekyll','assets/config.js','assets/app.js','assets/style.css',
          'app.py','inference_bridge.py','cnn_utils.py','multiview_inference.py',
          'recycling_advice.py','requirements.txt','.gitignore')
SECRET_EXT={'.pth','.pt','.joblib','.pkl','.onnx','.npy','.npz','.parquet','.pem','.p12','.pfx'}
PROTECTED_DIRS={'__pycache__','.venv','venv','dataset-resized'}
def main():
    issues=[]
    for name in REQUIRED:
        if not (ROOT/name).is_file(): issues.append('Thieu: '+name)
    if (ROOT/'index.html').exists():
        body=(ROOT/'index.html').read_text(encoding='utf-8')
        if '<html' not in body or 'assets/app.js' not in body: issues.append('index.html khong dung dinh dang')
    for p in ROOT.rglob('*'):
        if not p.is_file(): continue
        rel=p.relative_to(ROOT)
        if any(part in PROTECTED_DIRS for part in rel.parts): issues.append('Thu muc can loai: '+str(rel))
        if p.suffix.lower() in SECRET_EXT: issues.append('File mo hinh hoac rieng tu: '+str(rel))
        if p.name in ('.env','secrets.toml','credentials.json'): issues.append('File bi mat: '+str(rel))
        if p.stat().st_size > 25*1024*1024: issues.append('File >25MB: '+str(rel))
    if issues:
        print('[LOI] Phat hien van de:')
        for s in issues: print(' -',s)
        return 1
    print('[OK] Co index.html va cac file can thiet, khong co checkpoint/du lieu nhay cam theo duoi mo rong va vi tri da kiem tra.')
    print('[LUU Y] Day la kiem tra tu dong; hay ra soat file truoc khi cong khai.')
    return 0
if __name__=='__main__': sys.exit(main())
