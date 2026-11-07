"""Quick diagnostic for the AI02 V12 local project, without loading model weights."""
from pathlib import Path
import importlib.util
import sys

ROOT = Path(__file__).resolve().parent


def main():
    print("=" * 58)
    print("AI02 V12 - KIEM TRA MOI TRUONG")
    print("Thu muc :", ROOT)
    print("Python   :", sys.version.split()[0])
    print("=" * 58)
    for module in ("streamlit", "PIL", "numpy", "sklearn", "torch", "torchvision"):
        ok = importlib.util.find_spec(module) is not None
        print(("[OK]   " if ok else "[THIEU]"), module)
    for filename in ("app.py", "inference_bridge.py", "cnn_utils.py", "ui_v10_utils.py", "src/predict.py"):
        ok = (ROOT / filename).is_file()
        print(("[OK]   " if ok else "[THIEU]"), filename)
    print("\nCHECKPOINTS THUC TE:")
    model_dir = ROOT / "model"
    found = sorted(model_dir.glob("*.pth")) + sorted(model_dir.glob("*.joblib")) if model_dir.is_dir() else []
    if not found:
        print("[THIEU] Chua co checkpoint trong model/; web chua the du doan.")
    for path in found:
        print("[CO]   ", path.name, f"({path.stat().st_size / 1024**2:.1f} MB)")
    print("\nCAMERA: tren cung may, mo http://localhost:8501")
    print("IP LAN http://172.20.x.x:8501 co the bi chan quyen camera.")
    print("Neu mo web bi loi, chup anh thong bao trong Terminal.")


if __name__ == "__main__":
    main()
