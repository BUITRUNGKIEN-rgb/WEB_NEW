# SMART CAMPUS AI02 – Web V10 (trắng, xanh, cam)

## Phiên bản này có gì?

Đây là **nâng cấp giao diện và tính năng web** của AI02 V9. Bộ code Python huấn luyện, các tệp `.joblib` và `.pth` không bị thay đổi.

- **Nhận diện từng ảnh**: chọn ảnh hoặc camera, thông báo nhãn, xác suất 6 lớp, top-2, cảnh báo độ tự tin, gợi ý phân loại.
- **So sánh hai mô hình**: dùng cùng một ảnh, xem kết quả hai mô hình bên cạnh nhau; không nhầm so sánh một ảnh với Macro-F1 toàn tập.
- **Phân tích hàng loạt**: tải tối đa 20 ảnh mỗi lượt để tránh quá tải RAM/CPU, xuất CSV có dấu tiếng Việt.
- **Lịch sử phiên**: tối đa 150 bản ghi, có nút tải CSV/xóa; *không* lưu ảnh hay lịch sử lâu dài trên server.
- **Phương pháp & thực nghiệm**: giới thiệu bối cảnh, dữ liệu, hạn chế, chỉ hiện chỉ số thực tế khi có các tệp JSON trong `results/`, `results_cnn/`.
- **Giao diện**: trắng/xanh dương/cam, nhiều thẻ chức năng, tối ưu màn hình laptop và thuyết trình.

## Cách cài V10 trên Windows (đã có V9)

1. Giải nén ZIP.
2. Mở thư mục `AI02_V10_WEB_NANG_CAP`, nhấp đúp `00_CAP_NHAT_WEB_V10.bat`.
3. Khi hỏi đường dẫn dự án, nhấn Enter nếu dự án nằm tại:

   `D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02`

4. Bộ cài sao lưu `app.py` cũ vào `backup_v10/app.py` (nếu chưa có), sao chép `app.py` và `ui_v10_utils.py`, tạo file chạy `01_CHAY_WEB_V10.bat` trong dự án cũ.
5. Mở dự án cũ, nhấp đúp `01_CHAY_WEB_V10.bat`.
6. Mở http://localhost:8501.

**Không xóa hoặc thay đổi** thư mục `model/`, `data/`, `results/`. Nếu sử dụng CNN V9 bạn cần có file checkpoint đã huấn luyện `.pth`; nếu chỉ có hai file `.joblib` thì app vẫn chạy với Baseline/SVM, không bịa dự đoán CNN.

## Chạy bằng VS Code / PowerShell

```powershell
cd "D:\UNETI12_ODD3_AI02_V3_RA_SOAT_KY\UNETI12_ODD3_AI02"
..\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements_cnn.txt
..\.venv\Scripts\python.exe -m streamlit run app.py
```

Nếu `.venv` ở **trong** dự án thì thay `..\.venv` bằng `.\.venv`.

## Nếu muốn chạy V10 như dự án độc lập

Mở thư mục chứa `app.py` của ZIP trong VS Code, cài thư viện trong `requirements.txt`, rồi sao chép **các mô hình được huấn luyện hợp lệ** từ project cũ sang `model/`:

- `baseline.joblib`, `improved.joblib` (V4)
- `ai02_mobilenet_v3_large.pth`, `ai02_efficientnet_b2.pth`... (CNN, tùy bạn đã huấn luyện)

Không chép trọng số ngẫu nhiên/smoke test để demo thi. **Không cần chép bộ ảnh TrashNet** để chạy dự đoán.

## Nộp chung kết / đánh giá

V10 **không tự làm mô hình chính xác hơn**. Các số liệu phản biện phải đến từ quá trình đánh giá trên cùng tập validation. Không dùng một ảnh đúng để chứng minh CNN tốt hơn toàn bộ. Website không thay thế `slides.pdf` bắt buộc theo đề.

## Cách triển khai online

- GitHub lưu mã Python, Streamlit Community Cloud chạy `app.py` và phục vụ website `*.streamlit.app`.
- GitHub Pages (`github.io`) **không** chạy `app.py` trực tiếp; nếu buộc phải dùng GitHub Pages thì cần phiên bản web tĩnh riêng.
- Checkpoint `.joblib` cần nguồn đáng tin cậy và phiên bản thư viện phù hợp; không cho phép người dùng web tải checkpoint lên server để giải nén.
- Các checkpoint CNN cần CPU RAM đáng kể; một số tính năng phân tích hàng loạt có thể chậm trên máy miễn phí.

## Thành phần quan trọng

- `app.py`: giao diện Streamlit V10.
- `ui_v10_utils.py`: hiển thị xác suất, lịch sử, xuất CSV.
- `inference_bridge.py`, `cnn_utils.py`, `src/*`: phần dự đoán V9 được giữ nguyên.
- `00_CAP_NHAT_WEB_V10.bat`: chép V10 vào dự án cũ.
- `01_CHAY_WEB_V10.bat`: chạy Streamlit bằng `.venv` hiện có.

**Quyền riêng tư:** Khác GitHub Pages chạy cục bộ, khi triển khai Streamlit Cloud, ảnh tải lên sẽ được gửi tới máy chủ của dịch vụ để thực hiện dự đoán. Không tải ảnh cá nhân hoặc nhạy cảm; chỉ dùng ảnh rác minh họa.
