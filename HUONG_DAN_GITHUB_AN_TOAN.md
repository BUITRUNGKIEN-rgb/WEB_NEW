# Hướng dẫn GitHub an toàn · AI02 V13

## 1. Gói này chứa gì?

Đây là **bản sao mã nguồn V13**, không phải bản chép/ghi đè thư mục dự án trên máy bạn. Các file `.py` của V13 được giữ nguyên. Gói **không chứa ảnh TrashNet, kết quả đánh giá, dữ liệu CSV thực tế, `.joblib`, `.pth`, khóa truy cập hoặc môi trường ảo**. Bốn thư mục `data/`, `model/`, `results/`, `results_cnn/` chỉ có `README.txt` mô tả.

Có thể dùng để đưa **mã nguồn** lên GitHub, nhưng **không tự cung cấp dịch vụ dự đoán** nếu server không có checkpoint đã huấn luyện.

## 2. Cách an toàn nhất: tạo repository GitHub mới

1. Vào https://github.com/new , tạo repo **AI02-UNETI12-ODD3** (public/private tùy bạn); **đừng khởi tạo README/.gitignore mới** vì gói đã có.
2. Giải nén ZIP này vào **thư mục riêng**, ví dụ `D:\AI02_V13_GITHUB_SAFE`; **đừng giải nén chồng lên thư mục dữ liệu gốc**.
3. Mở thư mục vừa giải nén bằng VS Code → Terminal (PowerShell). Kiểm tra `dir app.py`, `dir .gitignore`.
4. Chạy lần lượt:

```powershell
git init
git branch -M main
git add .
py KIEM_TRA_GITHUB_AN_TOAN.py
git status --short
git commit -m "Add AI02 V13 source safely"
git remote add origin https://github.com/USERNAME/AI02-UNETI12-ODD3.git
git push -u origin main
```

Thay `USERNAME` bằng tài khoản GitHub của bạn và **thay URL bằng đúng liên kết repository mới**. Nếu Windows không có lệnh `py`, dùng `python KIEM_TRA_GITHUB_AN_TOAN.py`. Nếu chưa có Git, cài Git for Windows rồi mở lại VS Code. Khi đăng nhập, GitHub có thể mở trình duyệt hoặc yêu cầu credential manager; **không nhập mật khẩu GitHub thường vào ô password của Git**.

**Quan trọng:** Nếu công cụ kiểm tra báo `[BLOCK]`, **không commit và không push**. Kiểm tra danh sách staged rồi loại file nhạy cảm bằng `git restore --staged "duong-dan-file"`.

## 3. Nếu muốn push ngay trong thư mục dự án hiện có

*Ưu tiên cách 2 để không phải thao tác với dữ liệu gốc.* Nếu bạn vẫn muốn dùng dự án hiện có:

- Sao lưu ngoài repository trước.
- Chép **chỉ `.gitignore` và `KIEM_TRA_GITHUB_AN_TOAN.py`** từ bộ này vào **gốc repository** (nơi có `app.py`), sau đó `git add .` và chạy script kiểm tra trước khi commit.
- Nếu ảnh/dữ liệu/mô hình đã từng được `git add` trước khi thêm `.gitignore`, chúng có thể **vẫn đang được Git theo dõi**. Lệnh `git rm --cached --ignore-unmatch -r data model results results_cnn` chỉ bỏ theo dõi từ Git, **không xóa file vật lý ở máy**; nhưng vẫn cần kiểm tra `git status` trước khi commit. Nếu chúng đã được push trước đây thì xóa khỏi bản commit mới **không xóa được lịch sử cũ**; cần xử lý lịch sử repo riêng và thay khóa nếu có lộ secrets.

## 4. Cách kiểm tra sau khi push

Mở repo trên GitHub: cần thấy `app.py`, `train_cnn.py`, `recycling_advice.py`, `multiview_inference.py`, `src/` và các file hướng dẫn. Không được thấy ảnh trong `data/dataset-resized`, checkpoint thật trong `model`, file báo cáo hoặc `.streamlit/secrets.toml`.

## 5. GitHub Pages khác web Streamlit

**Không thể dùng GitHub Pages chạy `app.py` và EfficientNet-B2 trực tiếp.** GitHub là nơi lưu code. Để có link demo AI chạy trực tuyến cần server Python và checkpoint đã huấn luyện. Nếu dùng Streamlit Community Cloud, cần cân nhắc dung lượng/RAM của CNN và cơ chế lưu model phù hợp. Thông tin bí mật để ở `st.secrets`/cấu hình dịch vụ, không đẩy vào repo.

## 6. Dữ liệu quan trọng được giữ nguyên

Bộ này không chạy lệnh sửa, di chuyển hoặc xóa `data/`, `model/`, `results/`, `results_cnn/` của bạn. `.gitignore` ngăn Git tự theo dõi các dữ liệu đó nếu chúng chưa được theo dõi từ trước; bản sao trong GitHub **không phải bản sao lưu dữ liệu gốc**.
