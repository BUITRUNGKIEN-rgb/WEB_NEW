# AI02 V8 – Sửa tình trạng đổi giao diện nhưng dự đoán vẫn như cũ

**Triệu chứng:** Lon kim loại bị nhận diện `glass` 49,0% và `metal` 35,6%, giống kết quả từ mô hình V4 trước khi nâng cấp.

## 1. Kiểm tra đã có CNN chưa

Trong thư mục dự án AI02 chạy `07_KIEM_TRA_MODEL.bat` hoặc:

```powershell
..\.venv\Scripts\python.exe kiem_tra_model_v8.py
```

Nếu thông báo thiếu `model/ai02_mobilenet_v3_large.pth`, **bạn vẫn đang chạy SVM V4**, không phải CNN V5. Không có mô hình nào tự cải thiện chỉ bằng thay đổi giao diện.

## 2. Nếu chưa có CNN, huấn luyện lần đầu

Đảm bảo đủ 6 lớp TrashNet trong `data/dataset-resized` rồi chạy:

```powershell
..\.venv\Scripts\python.exe train_cnn.py --images "data/dataset-resized" --arch mobilenet_v3_large --split-manifest "results/split_manifest.csv" --model-dir model --results results_cnn --batch-size 8
```

Chạy trên CPU vẫn được nhưng chậm; lần đầu cần Internet để tải pretrained weights. Không dùng cờ `--no-pretrained` cho kết quả dự thi.

Sau khi huấn luyện kết thúc, kiểm tra có `model/ai02_mobilenet_v3_large.pth` và `results_cnn/metrics_mobilenet_v3_large.json`.

## 3. Chạy lại web và CHỌN đúng CNN

```powershell
..\.venv\Scripts\python.exe -m streamlit run app.py
```

Ở thanh sidebar chọn **CNN V5 · MobileNetV3-Large** thay vì **SVM cải tiến V4**. Giao diện bản vá hiện hiển thị rõ mô hình đang được chọn và dùng khi dự đoán.

## 4. So sánh trên cùng một ảnh

```powershell
..\.venv\Scripts\python.exe kiem_tra_model_v8.py --image "data/dataset-resized/metal/metal1.jpg"
```

Thay tên ảnh bằng ảnh thực sự có trên máy. Chương trình in dự đoán của từng mô hình với cùng ảnh.

## 5. Chứng minh cải tiến theo AI02

Chạy `compare_results.py` sau khi CNN đã tạo `results_cnn/predictions_mobilenet_v3_large.csv`, nếu có kết quả V4 ở `results/validation_predictions.csv`. Chỉ so sánh khi cùng tập validation. Quan sát Macro-F1, F1 từng lớp và số lỗi `metal → glass`. Một ảnh dự đoán đúng hơn không đủ chứng minh mô hình tổng thể tốt hơn.

**Đừng đổi thủ công nhãn glass thành metal, hay thêm quy tắc dựa vào tên file `metal1.jpg`: đó không phải cải tiến học máy hợp lệ.**
