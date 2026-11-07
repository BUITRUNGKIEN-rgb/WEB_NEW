# AI02 – Web V13: Tư vấn tái chế + Nhận diện đa góc

Đội **UNETI12 – ODD3** · Olympic AI UNETI 2026 · Bài AI02 (TrashNet sáu loại).

## Thay đổi

**1. ♻️ Có thể tái chế không?**

- Sau mỗi dự đoán, web hiển thị **tiềm năng tái chế**, giải thích và cách xử lý.
- Thanh bên trái có ba trường do người dùng **tự khai báo**: tình trạng sạch/bẩn, điểm thu gom nhận đúng vật phẩm hay chưa, và vật phẩm nguy hại/thu gom riêng.
- Không đoán “chắc chắn tái chế được” chỉ từ nhãn `metal`, `plastic`...; nếu mô hình không chắc chắn hoặc lớp `trash`, web sẽ ghi **chưa thể kết luận**.
- Không có model 7 lớp / model phân loại tái chế được/không: đây là **lớp quy tắc tham khảo** dựa trên nhóm vật liệu của mô hình hiện có.
- Dữ liệu có điều kiện theo hướng dẫn chung: https://www.epa.gov/recycle/how-do-i-recycle-common-recyclables và https://www.epa.gov/recycle/frequent-questions-recycling . **Không thay thế quy định tại Việt Nam/nơi thu gom cụ thể**.

**2. Nhận diện đa góc 2–6 ảnh cùng vật thể**

- Chọn mục **Nhận diện đa góc** trong thanh bên trái.
- Chụp **cùng một vật** từ 2–6 hướng thật: trước, trái/phải, từ trên...; tải nhiều ảnh lên (không cần bật camera ở địa chỉ IP HTTP).
- Mô hình V9 thật được chạy *riêng* trên mỗi ảnh, rồi trung bình xác suất của 6 nhãn (**multi-view soft voting**).
- Cảnh báo các góc bất đồng nhãn và tỷ lệ đồng thuận, trình bày bảng kết quả từng góc.
- Loại ảnh trùng hệt nhau theo SHA-256; ảnh quá tối/cháy sáng có nhắc chụp lại.
- **Đa góc có thể làm kết quả ổn định hơn, nhưng không được bảo đảm chính xác hơn**, phải đo trên tập kiểm tra đa góc riêng. Ảnh cùng một vật được tính là *một mẫu kiểm tra*, không được đếm thành nhiều mẫu độc lập.

**3. Vẫn giữ đầy đủ tính năng V12**

- Nhận diện ảnh/camera (mặc định tải ảnh), so sánh hai mô hình, xử lý hàng loạt, lịch sử và CSV, phương pháp/metrics thật.
- Không thay đổi `train_cnn.py`, `cnn_utils.py`, checkpoint `.pth`/`.joblib`, dữ liệu hoặc chỉ số Macro-F1 đã lưu.
- Thư mục `model`, `data`, `results`, `results_cnn` của dự án cũ **không bị xóa**.

## Cài đặt khi bạn đã có V9–V12

1. Tải ZIP **AI02_WEB_V13_CAP_NHAT_NHANH.zip**, chọn Extract All.
2. Mở thư mục `AI02_V13_CAP_NHAT_NHANH`, chạy `00_CAP_NHAT_WEB_V13.bat`.
3. Khi hỏi đường dẫn, nhấn **Enter** nếu dự án cũ ở
   `D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02`.
4. Chương trình sao lưu `app.py` vào `backup_ui/`, thay `app.py`, đồng bộ `ui_v10_utils.py`, thêm `recycling_advice.py`, `multiview_inference.py`, các BAT.
5. Dừng Streamlit cũ bằng Ctrl+C.
6. Trong **thư mục dự án cũ**, nhấp đúp `01_CHAY_LOCAL_V13.bat`; mở http://localhost:8501 .

### Chạy bằng VS Code

```powershell
cd "D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02"
..\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Nếu `.venv` nằm trong dự án, đổi `..\.venv` thành `.\.venv`.

### Sử dụng

1. Trong sidebar, chọn checkpoint **CNN V9 EfficientNet-B2** nếu bạn đã huấn luyện thực và `.pth` nằm ở `model/`.
2. **Nhận diện ảnh**: tải một ảnh → Phân tích → xem kết quả + thẻ **Có thể tái chế không?**.
3. **Nhận diện đa góc**: tải 2–6 ảnh **cùng vật** (ví dụ cùng một lon) → đánh dấu xác nhận → Nhận diện đa góc → xem nhãn tổng hợp, đồng thuận và từng góc.
4. Thay đổi độ sạch và thông tin điểm thu gom ở **♻️ Điều kiện tái chế** để cập nhật tư vấn ngay.
5. **Lịch sử & Xuất CSV**: lưu dự đoán trong phiên, có thêm cột trạng thái tái chế và số góc chụp.

## Tính trung thực khi trình bày với Ban Giám khảo

- Độ tin cậy dự đoán chỉ là xác suất do mô hình trả về, không được xem là xác suất “được phép tái chế”.
- Độ đồng thuận giữa các góc **không phải accuracy**.
- Nếu ảnh lon kim loại vẫn bị nhận sai, cần kiểm tra mô hình và thử góc chụp khác; không được tuyên bố đã cải thiện Macro-F1 khi chưa có phép đo.
- Với pin, đồ điện tử, bóng đèn, hóa chất, vật sắc nhọn, cần thu gom riêng; mô hình chỉ có 6 lớp nên **không tự phát hiện đáng tin cậy** những ngoại lệ này.

## Kiểm tra

Chạy `03_KIEM_TRA_V13.bat` trên dự án đã cập nhật. Kiểm thử thuần Python (nếu có pytest):

```powershell
..\.venv\Scripts\python.exe -m pytest tests\test_v13.py -q
```

Không có checkpoint huấn luyện thật trong gói ZIP; không nạp mô hình lạ từ Internet.
