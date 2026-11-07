# SMART CAMPUS AI02 – WEB V12 ỔN ĐỊNH

Bản cập nhật dành cho **UNETI12 – ODD3**. Thay giao diện V11 nhưng **giữ nguyên** mô hình `.joblib`, `.pth`, dữ liệu, báo cáo và mã huấn luyện V9.

## Tại sao camera trong ảnh bị lỗi?

Ảnh chụp màn hình của bạn mở URL `http://172.20.10.2:8501`. Đây là IP trong mạng LAN và đang dùng **HTTP không bảo mật**. Trình duyệt thường chỉ cho phép camera khi truy cập **HTTPS hoặc http://localhost**. Việc sửa Python không thể bỏ qua hạn chế này của trình duyệt.

## V12 thay đổi gì?

- Mặc định **Tải ảnh từ máy**, không bật camera tự động; giao diện không còn khung trắng yêu cầu camera ngay khi mở.
- Camera là một tùy chọn riêng. Có hướng dẫn `localhost`/HTTPS và xác nhận trước khi tải widget camera.
- Chạy **LOCAL** (`127.0.0.1`) giúp camera dễ hoạt động hơn trên chính laptop/PC đang chạy ứng dụng. Trình duyệt vẫn phải được cấp quyền.
- Chạy **LAN** (`0.0.0.0`) giúp máy/điện thoại khác trong cùng mạng tải ảnh để phân tích, nhưng camera của chúng qua HTTP IP có thể bị trình duyệt chặn.
- Ảnh được kiểm tra dung lượng, số pixel, định dạng, chiều EXIF; lỗi mô hình/thư viện có hướng dẫn sửa.
- Giữ 5 mục: nhận diện, so sánh, hàng loạt, lịch sử CSV, dữ liệu và phương pháp.
- Kết quả chỉ lấy từ checkpoint thật qua `inference_bridge.py`. Không tạo dự đoán giả.

## Cập nhật vào dự án cũ (khuyến nghị)

1. Giải nén `AI02_WEB_V12_CAP_NHAT_ON_DINH.zip`.
2. Vào thư mục `AI02_V12_WEB_ON_DINH`, nhấp đúp `00_CAP_NHAT_WEB_V12.bat`.
3. Nhấn Enter nếu dự án tại `D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02`.
4. Đợi thông báo `[OK]`. Tool sao lưu `app.py` vào `backup_ui/`.
5. Tắt Streamlit cũ bằng Ctrl+C.
6. Trong thư mục dự án cũ, nhấp đúp `01_CHAY_LOCAL_V12.bat`.
7. **Mở đúng `http://localhost:8501`** (không dùng địa chỉ `172.20.10.2:8501` để bật camera).
8. Chọn "Tải ảnh từ máy", chọn checkpoint EfficientNet-B2 (nếu có), tải ảnh và nhấn **PHÂN TÍCH HÌNH ẢNH**.

## Cách chạy bằng VS Code

```powershell
cd "D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02"
..\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Nếu `.venv` nằm trong thư mục dự án, dùng `.\.venv\Scripts\python.exe` thay vì `..\.venv\Scripts\python.exe`.

**Chẩn đoán:** nhấp đúp `03_KIEM_TRA_V12.bat` hoặc chạy `..\.venv\Scripts\python.exe kiem_tra_v12.py` trong dự án.

## Điện thoại / máy khác trong mạng LAN

Chạy `02_CHAY_MANG_LAN_V12.bat` trên máy chủ, mở URL Network như `http://172.20.10.2:8501` từ máy khác, dùng **Tải ảnh từ máy**. Để dùng camera từ thiết bị khác, cần triển khai HTTPS với chứng chỉ hợp lệ. Lưu ý việc chia sẻ LAN là chia sẻ ứng dụng với các thiết bị trong mạng tin cậy.

## Không thay đổi những gì?

Bản này KHÔNG huấn luyện lại EfficientNet-B2, KHÔNG thay đổi Macro-F1 và KHÔNG chỉnh sửa file checkpoint. Nếu CNN vẫn dự đoán sai, cần cải thiện/đánh giá mô hình riêng.
