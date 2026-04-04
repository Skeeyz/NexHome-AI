# 🏘️ NexHome AI - Smart Real Estate Engine
> **Evolution of Estate** | Hệ thống định giá và phân tích bất động sản thông minh dựa trên trí tuệ nhân tạo.

[![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io/)
[![ML Framework](https://img.shields.io/badge/ML-XGBoost%20v2.1.0-6366f1.svg)](https://xgboost.readthedocs.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**NexHome AI** là nền tảng PropTech (Property Technology) hiện đại, giúp người dùng giải quyết bài toán định giá bất động sản tại Việt Nam. Bằng cách kết hợp thuật toán **XGBoost** tiên tiến và bộ dữ liệu hơn 22,000 niêm yết thực tế của Batdongsan.com.vn(cập nhật đến năm 2024), hệ thống cung cấp góc nhìn khách quan và chính xác về giá trị tài sản.

---

## ✨ Tính năng nổi bật

* **📊 Market Intelligence:** Phân tích trực quan mặt bằng giá theo khu vực, tỷ lệ pháp lý và biến động thị trường thời gian thực.
* **🔮 NexHome AI Engine:** Định giá chính xác dựa trên 10 tham số đầu vào (Diện tích, mặt tiền, đường vào, pháp lý, vị trí...).
* **⚖️ Đối chiếu BĐS:** So sánh "đối đầu" giữa hai bất động sản để tìm ra lựa chọn tối ưu về giá trị và tiềm năng.
* **📂 Workspace & History:** Hệ thống tự động lưu trữ lịch sử tra cứu vào file dữ liệu cục bộ (`.csv`), giúp quản lý và theo dõi danh mục dễ dàng.
* **💎 Giao diện Modern UI:** Thiết kế Top Branding Bar chuyên nghiệp, tối ưu trải nghiệm người dùng trên nền tảng Web.

---

## 🛠 Công nghệ cốt lõi

| Thành phần | Công nghệ sử dụng |
| :--- | :--- |
| **Giao diện** | Streamlit (Custom HTML/CSS) |
| **Mô hình AI** | XGBoost Regressor |
| **Xử lý dữ liệu** | Pandas, Scikit-learn, Numpy |
| **Trực quan hóa** | Plotly (Interative Charts) |
| **Lưu trữ** | CSV Persistent Storage |

---

## 📁 Cấu trúc dự án

```text
NexHome-AI/
├── data/
│   ├── VN_House_price_Clean2.csv   # Dữ liệu thị trường gốc
│   └── user_history.csv           # Lịch sử tra cứu (Tự động tạo)
├── models/
│   └── model_xgb.json             # Trí tuệ nhân tạo đã huấn luyện
├── utils/
│   ├── data_helper.py             # Hậu cần dữ liệu & Lưu trữ
│   └── model_loader.py            # Quản lý và thực thi mô hình AI
├── views/
│   ├── 1_Market_Analysis.py       # Phân tích thị trường
│   ├── 2_Predictions.py           # Định giá thông minh
│   ├── 3_Comparison.py            # So sánh đối đầu
│   └── 4_Histories.py             # Workspace lịch sử
├── app.py                         # Cổng khởi chạy chính (Main Entry)
└── requirements.txt               # Danh sách thư viện hệ thống
```
---
## 🚀 Hướng dẫn cài đặt và chạy

### 1. Yêu cầu hệ thống
* Đã cài đặt **Python 3.9** trở lên.
* Đã cài đặt môi trường ảo (Khuyên dùng để tránh xung đột thư viện).

### 2. Cài đặt
Tải dự án về máy và cài đặt các thư viện cần thiết:

```bash
# Clone dự án từ GitHub
git clone https://github.com/Skeeyz/NexHome-AI.git
cd NexHome-AI

# Cài đặt các thư viện hệ thống
pip install -r requirements.txt
```

### 2. Khởi chạy ứng dụng
```bash
streamlit run app.py
```
---
## 🧠 Quy trình huấn luyện (Notebook)
* Dự án đi kèm file mayhoc.ipynb đóng vai trò là phòng thí nghiệm dữ liệu chuyên sâu, minh họa quy trình xây dựng AI bài bản:

* Tiền xử lý: Làm sạch dữ liệu, xử lý các điểm dị biệt (Outliers) và điền giá trị thiếu (Imputation).

* Mã hóa (Encoding): Chuyển đổi dữ liệu phân loại (Quận, Thành phố, Pháp lý) bằng LabelEncoder để mô hình máy học có thể xử lý.

* Huấn luyện (Training): Đánh giá và huấn luyện đồng thời các thuật toán mạnh mẽ như Random Forest và XGBoost.

* Tối ưu hóa (Optimization): Tinh chỉnh các siêu tham số (Hyperparameters) thông qua bộ lọc GridSearchCV để đạt hiệu suất cao nhất.

* Xuất bản (Export): Xuất mô hình sang định dạng .json để ứng dụng Streamlit có thể sử dụng trực tiếp mà không cần huấn luyện lại mỗi khi khởi động.
