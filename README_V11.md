# SMART CAMPUS AI02 – GIAO DIỆN V11 DỄ NHÌN

**Bản V11 chỉ cải thiện giao diện Streamlit**, không thay đổi thuật toán, mô hình, kết quả Macro-F1 hay file huấn luyện.

## Thay đổi so với V10
- Đầu trang ngắn hơn; không còn các ô thống kê lớn làm che khuất ảnh và nút dự đoán.
- Hai cột chính rõ ràng: **chọn ảnh** (trái) và **kết quả AI** (phải).
- Tăng độ tương phản chữ, giữ tone **trắng – xanh dương – cam**; font và khoảng cách dễ đọc.
- Thanh xác suất gọn, nền xám nhạt; nhóm dự đoán cao nhất tô cam, không còn nền cam kéo dài gây nhầm lẫn.
- Cảnh báo ảnh khó nhận diện, top-2 và khuyến nghị được giữ lại.
- Giữ đủ các mục: **Nhận diện ảnh**, **So sánh mô hình**, **Phân tích hàng loạt**, **Lịch sử & Xuất CSV**, **Dữ liệu & Phương pháp**.
- Phù hợp màn hình laptop và trình chiếu. Không tạo xác suất hoặc nhãn giả.

## Cài trên Windows khi đã có V9/V10
1. Giải nén ZIP, mở thư mục `AI02_WEB_V11_DE_NHIN`.
2. Chạy `00_CAP_NHAT_GIAO_DIEN_V11.bat`.
3. Nhấn Enter nếu dự án cũ tại `D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02`; nếu khác, dán đường dẫn thư mục dự án thực tế.
4. Bản cập nhật **sao lưu `app.py` cũ** trong `backup_ui/`, chép `app.py`, `ui_v10_utils.py`, cấu hình theme và lệnh chạy. Không động đến `model/`, `data/`, `results/` hoặc mã huấn luyện.
5. Tắt Streamlit đang chạy bằng `Ctrl+C`. Chạy `01_CHAY_WEB_V11.bat` trong thư mục dự án hoặc mở Terminal với lệnh:

```powershell
cd "D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02"
..\.venv\Scripts\python.exe -m streamlit run app.py
```

6. Mở `http://localhost:8501`, nhấn Ctrl+Shift+R nếu còn giao diện cũ.

## Nếu dùng ZIP full như dự án mới
Cần thêm file mô hình thật trong `model/`: `baseline.joblib`, `improved.joblib`, hoặc checkpoint `.pth` tương ứng. Gói này không bao gồm trọng số của bạn và không huấn luyện thay bạn.

## Lưu ý
- **Độ chính xác không đổi** khi chỉ cập nhật giao diện. Để cải thiện cần huấn luyện và đánh giá mô hình trên TrashNet thật.
- Ảnh tải lên Streamlit Cloud được chuyển đến máy chủ để dự đoán. Mã giao diện không chủ động lưu ảnh vào dữ liệu train.
- GitHub Pages không chạy trực tiếp `app.py`; dùng Streamlit Community Cloud cho bản Python online.
