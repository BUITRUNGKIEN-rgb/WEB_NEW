# AI02 V9 – nâng cấp dự đoán, vẫn tuân thủ đề AI02

## Mục tiêu

V9 giữ **Baseline BTC (HOG + RGB + Logistic Regression)** và **SVM V4** để đối chứng. Bổ sung hai lựa chọn pretrained CNN **EfficientNet-B2** và **ConvNeXt-Tiny**, tùy chọn trung bình xác suất của hai CNN và TTA lật ngang *chỉ nếu Macro-F1 trên tập internal-dev cải thiện*. Mọi lựa chọn huấn luyện/tối ưu dựa trên train + internal-dev, không tối ưu dựa trên nhãn validation cuối.

**Không có mô hình đạt độ chính xác tuyệt đối. Không dùng một ảnh kim loại để kết luận chung.** CNN cần huấn luyện trên TrashNet thật; ZIP không có file `.pth` đã huấn luyện.

## Cài vào dự án cũ trên Windows

1. Giải nén ZIP, mở thư mục `AI02_V9_DU_DOAN_NANG_CAO`.
2. Chạy `00_CAP_NHAT_VAO_DU_AN_CU.bat`; Enter để dùng đường dẫn mặc định `D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02`. File cũ được sao lưu tại `backup_before_v9/`; thư mục dữ liệu và mô hình giữ nguyên.
3. Mở dự án cũ trong VS Code, Terminal ở thư mục `UNETI12_ODD3_AI02`.
4. Nếu `.venv` nằm thư mục cha (theo máy bạn), cài: `..\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements_cnn.txt`.
5. Chạy `08_HUAN_LUYEN_V9_B2.bat` trong thư mục dự án (khuyến nghị trước). Lần đầu cần Internet tải pretrained weights.
6. Có GPU/bộ nhớ phù hợp thì chạy tiếp `09_HUAN_LUYEN_V9_CONVNEXT.bat` (tùy chọn; nặng hơn).
7. Kiểm tra `model\ai02_efficientnet_b2.pth` và `results_cnn\metrics_efficientnet_b2.json`. Nếu thấy checkpoint **SMOKE_NOT_FOR_SUBMISSION** thì không dùng để thi.
8. Mở web: `..\.venv\Scripts\python.exe -m streamlit run app.py` rồi mở `http://localhost:8501`. Chọn *CNN V9 · EfficientNet-B2* (hoặc ConvNeXt/Ensemble nếu đã có).
9. Chạy `11_SO_SANH_V4_V9.bat` để so sánh cùng validation. Nếu công cụ báo tập validation khác nhau, không công bố so sánh trực tiếp.

## Lệnh PowerShell đầy đủ

```powershell
cd "D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02"
..\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements_cnn.txt
..\.venv\Scripts\python.exe train_cnn.py --arch efficientnet_b2 --images "data/dataset-resized" --split-manifest "results/split_manifest.csv" --model-dir model --results results_cnn --batch-size 8 --audit-near-duplicates
..\.venv\Scripts\python.exe kiem_tra_model_v9.py
..\.venv\Scripts\python.exe -m streamlit run app.py
```

## Kiểm chứng khoa học

- Dùng **cùng validation V4** nếu có `results/split_manifest.csv` (cần khớp từng ảnh).
- Chọn epoch, TTA, hệ số nhiệt độ xác suất trên **internal-dev** trích từ train; không sử dụng nhãn validation cuối để tối ưu.
- Báo cáo Macro-F1 và confusion matrix; đặc biệt số lần **metal bị nhầm glass** và **glass bị nhầm metal**.
- Nếu `near_duplicate_review.json` có ứng viên ảnh gần trùng xuyên tập, kiểm tra ảnh gốc bằng mắt; báo cáo hạn chế và không tự coi chúng là ảnh trùng thật.
- Khi làm ensemble, hai CNN phải cùng thứ tự lớp; chương trình đã kiểm tra 6 nhãn. Trung bình xác suất đều; không chọn trọng số bằng validation.
- Dữ liệu TrashNet nền đơn giản. Ảnh nhiều vật thể, nền phức tạp có thể sai; khi top 2 gần nhau, giao diện cảnh báo để người dùng tự kiểm tra.

## Nguồn pretrained

- Torchvision model docs: https://docs.pytorch.org/vision/main/models
- TrashNet: https://github.com/garythung/trashnet

## Các file liên quan

- `cnn_utils.py`: CNN 4 kiến trúc + preprocessing đúng kích thước + TTA khi checkpoint bật.
- `train_cnn.py`: đào tạo, internal-dev, lựa chọn TTA, calibration, holdout final.
- `inference_bridge.py`: phát hiện CNN V9/V5, SVM và Baseline để dùng cùng `app.py`.
- `compare_results_v9.py`: so sánh paired V9 với V4 (không dùng validation để chỉnh mô hình).
- `kiem_tra_model_v9.py`: chẩn đoán checkpoint sẵn có.

Nếu dùng CPU, EfficientNet-B2 có thể cần nhiều thời gian; ConvNeXt-Tiny thường nặng hơn. Có thể giảm `--batch-size 8` xuống `4` khi hết bộ nhớ. **Đừng nói AI chính xác 100%** khi chưa có bằng chứng và cũng không được dùng nhãn validation để điều chỉnh nhiều lần nhằm đẹp điểm.
