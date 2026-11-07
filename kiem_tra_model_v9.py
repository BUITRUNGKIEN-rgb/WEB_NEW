# -*- coding: utf-8 -*-
"""Chẩn đoán AI02 V9: mô hình được nạp và đầu ra của từng mô hình.
Dùng với các checkpoint do chính bạn huấn luyện, không nạp joblib lạ.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--image',default='',help='Ảnh rác để so sánh, ví dụ data/dataset-resized/metal/metal1.jpg')
    a=ap.parse_args()
    root=Path(__file__).resolve().parent
    print('\n'+'='*62)
    print(' KIỂM TRA THỰC TẾ MÔ HÌNH SMART CAMPUS AI02 V9')
    print('='*62)
    print('Thư mục dự án:',root)
    model_dir=root/'model'
    for filename in ('baseline.joblib','improved.joblib','ai02_mobilenet_v3_large.pth','ai02_efficientnet_b0.pth','ai02_efficientnet_b2.pth','ai02_convnext_tiny.pth'):
        f=model_dir/filename
        if f.is_file():
            print(f'[CÓ] {filename} | {f.stat().st_size/(1024*1024):.2f} MiB')
        else:
            print(f'[THIẾU] {filename}')
    from inference_bridge import discover_models
    choices=discover_models(str(model_dir))
    print('\nCác mô hình mà app.py có thể chọn:')
    for n,m in enumerate(choices,1): print(f'  {n}. {m["name"]} | {[str(p.name) for p in m["paths"]]}')
    hascnn=any(c['kind']=='cnn' for c in choices)
    if not hascnn:
        print('\n[CẦN LÀM] Chưa có .pth: CNN chưa được cài đặt.')
        if any(c['kind']=='classic' for c in choices):
            print('App sẽ dùng mô hình V4 còn sẵn, dù giao diện đã đổi.')
        print('Chạy 02_HUAN_LUYEN_CNN.bat hoặc lệnh train_cnn.py trong README.')
    else:
        print('\n[OK] Có CNN. Hãy CHỌN CNN trong sidebar Streamlit; không chọn SVM V4.')
    metrics=root/'results_cnn/metrics_mobilenet_v3_large.json'
    if metrics.is_file():
        try:
            d=json.loads(metrics.read_text(encoding='utf8'))
            print('Kết quả CNN validation Macro-F1:',d.get('final_val_macro_f1','chưa có'))
            print('Metal -> glass (validation):',d.get('metal_as_glass','chưa có'))
            if d.get('experimental_mode')=='SMOKE_NOT_FOR_SUBMISSION':
                print('[CẢNH BÁO] Checkpoint/báo cáo kiểm thử giả lập không được sử dụng dự thi.')
        except (OSError,ValueError) as e: print('Không đọc được metrics:',e)
    else:
        print('[THIẾU] results_cnn/metrics_mobilenet_v3_large.json')
    if a.image:
        img=Path(a.image)
        if not img.is_absolute(): img=root/img
        if not img.is_file():
            print('[LỖI] Không thấy ảnh:',img)
            return 2
        from PIL import Image
        from inference_bridge import predict_pil
        with Image.open(img) as original:
            im=original.convert('RGB')
        print('\nĐối chiếu cùng một ảnh:',img)
        for m in choices:
            try:
                out=predict_pil(im,m)
                ranked=sorted(out['probabilities'].items(),key=lambda p:-p[1])
                labels=', '.join(f'{x}: {v*100:.1f}%' for x,v in ranked[:3])
                print(f'  {m["name"]}: {out["label_vi"]} ({labels})')
            except Exception as e:
                print(f'  [KHÔNG CHẠY ĐƯỢC] {m["name"]}: {e}')
    print('\nLƯU Ý: Không thể bảo đảm chính xác tuyệt đối trên tất cả ảnh.')
    return 0

if __name__=='__main__':
    raise SystemExit(main())
