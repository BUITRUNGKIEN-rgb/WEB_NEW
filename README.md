# AI02 – Trường học xanh | UNETI12 – ODD3

Bộ mã nguồn **GitHub Pages + Streamlit**, chuẩn bị để đưa lên repository `BUITRUNGKIEN-rgb/AIX_Web_App`.

## Hai phần, hai địa chỉ

1. **GitHub Pages:** file [`index.html`](index.html) là **trang giới thiệu**. Không cần Python, không còn lỗi 404 do thiếu `index.html` nếu Pages được cấu hình đúng.
2. **Streamlit:** [`app.py`](app.py) là **ứng dụng nhận diện rác thật**. Cần deploy từ GitHub trên [Streamlit Community Cloud](https://share.streamlit.io/) hoặc máy chủ Python tương đương, và cần checkpoint thật để đưa ra dự đoán.

GitHub Pages **không chạy Python, Torch hoặc checkpoint `.pth`/`.joblib`**. Trang tĩnh không tự phân loại ảnh và không sinh dự đoán giả.

### Kết nối nút “Mở AI” trên Pages

Sau khi có URL thật `https://ten-ung-dung.streamlit.app`, mở [`assets/config.js`](assets/config.js), thay:

```js
streamlitUrl: "",
```

thành:

```js
streamlitUrl: "https://ten-ung-dung.streamlit.app",
```

Commit thay đổi lên GitHub. **Đừng dùng URL mẫu trong thực tế.**

## Thiết lập GitHub Pages tránh 404

Vào **Settings → Pages** trên GitHub, trong **Build and deployment** chọn **Deploy from a branch**, Branch `main`, Folder `/(root)`, rồi Save.

Nếu repository `AIX_Web_App` của bạn bật Pages và cấu hình đúng, địa chỉ dự kiến là:

`https://buitrungkien-rgb.github.io/AIX_Web_App/`

(Đây là dạng URL suy ra từ tên tài khoản và repository, **chưa phải xác nhận trang đã triển khai thành công**.)

## Triển khai AI thật trên Streamlit Cloud

- **Repository:** `BUITRUNGKIEN-rgb/AIX_Web_App`
- **Branch:** `main`
- **Main file path:** `app.py`
- **Python:** 3.12 (chọn trong Advanced settings khi cần).
- **Dependencies:** `requirements.txt` tại thư mục gốc.

**Quan trọng:** Mã nguồn không kèm bộ ảnh TrashNet hay checkpoint đã huấn luyện. Nếu thiếu `.pth`/`.joblib` trên máy chủ, Streamlit có thể hiển thị giao diện nhưng **không thể dự đoán thật**. Chỉ sử dụng checkpoint do đội huấn luyện và xác thực nguồn, không tải mô hình `.pth`/`.joblib` không tin cậy.

## Chạy nhận diện trên máy Windows

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address 127.0.0.1 --server.port 8501
```

Đặt checkpoint thật vào `model/`. Đối với `AIX_Web_App`, có thể mở GitHub Pages và Streamlit độc lập, rồi liên kết từ Pages sang Streamlit.

## Tính năng AI02

- Phân loại 6 lớp TrashNet; cảnh báo mức chắc chắn tương đối.
- Tổng hợp xác suất cho 2–6 góc chụp của cùng một vật.
- Tư vấn tái chế có điều kiện (phụ thuộc mức độ sạch, quy định điểm thu gom).
- So sánh mô hình, phân tích nhiều ảnh và xuất CSV phiên.

## Bảo vệ dữ liệu quan trọng

`.gitignore` loại trừ dữ liệu ảnh, checkpoint `.pth`/`.joblib`, kết quả thực nghiệm và cấu hình bí mật khi dùng Git thông thường. **Kéo thả trực tiếp bằng trình duyệt GitHub không áp dụng quy tắc `.gitignore`**, vì vậy chỉ upload đúng bộ mã ZIP này, không kéo thả dự án huấn luyện trên ổ D.

Chạy `python KIEM_TRA_GOI_TRUOC_UPLOAD.py` nếu muốn kiểm tra tự động. Đọc [`HUONG_DAN_DAY_GITHUB.txt`](HUONG_DAN_DAY_GITHUB.txt) để xem hướng dẫn ngắn gọn từng bước.

Xem thêm [`README_V13.md`](README_V13.md) để hiểu cách hoạt động của mô hình và các giới hạn khoa học.
