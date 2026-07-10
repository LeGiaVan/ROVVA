# 🏨 ROVVA — Smart Stay Platform

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Framework](https://img.shields.io/badge/flask-latest-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-Educational-orange.svg)]()

> Nền tảng đặt phòng homestay và khách sạn thông minh, kết hợp AI để tối ưu trải nghiệm tìm kiếm và hỗ trợ vận hành. Xây dựng dựa trên Flask Framework và kiến trúc Server-Side Rendering (SSR).

Hệ thống được thiết kế tối ưu cho 3 nhóm người dùng: **Customer**, **Host** và **Admin**, cung cấp trải nghiệm liền mạch từ khâu tìm kiếm, đặt phòng đến vận hành và quản trị hệ thống.

---

## 🌟 Các tính năng nổi bật

### Dành cho Khách hàng (Customer)
- **🧠 Smart Match (Tìm kiếm bằng ngôn ngữ tự nhiên):** Ứng dụng thuật toán TF-IDF và Cosine Similarity giúp người dùng tìm kiếm phòng thông qua các đoạn mô tả dài bằng tiếng Việt (ví dụ: *"Tôi muốn một căn hộ có ban công view biển, gần trung tâm cho 2 người"*).
- **🛒 Luồng đặt phòng mượt mà:** Từ việc tìm kiếm, xem chi tiết phòng, kiểm tra tình trạng trống, giữ phòng, thanh toán mô phỏng (mock payment), cho đến xác nhận booking.
- **🖼️ Hiển thị media tối ưu:** Hệ thống quản lý hình ảnh thông minh cho cơ sở lưu trú, phòng và avatar người dùng, có cơ chế fallback placeholder khi thiếu ảnh.

### Dành cho Chủ nhà (Host)
- **🤖 Host Copilot (Trợ lý vận hành thông minh):** Cung cấp các phân tích dữ liệu chuyên sâu:
  - Phân tích chân dung khách hàng (Customer Persona).
  - Radar cảnh báo bảo trì cơ sở vật chất.
  - Gợi ý tối ưu giá bán và doanh thu (Revenue suggestions).
- **📊 Quản lý toàn diện:** Bảng điều khiển (dashboard) trực quan giúp quản lý cơ sở lưu trú, danh sách phòng, và theo dõi booking hiệu quả.

### Dành cho Quản trị viên (Admin)
- **⚙️ Admin Panel:** Giao diện quản lý tập trung, giám sát toàn bộ hoạt động của hệ thống, quản lý người dùng, cơ sở lưu trú và các giao dịch.

---

## 🛠️ Công nghệ sử dụng (Tech Stack)

Hệ thống được phát triển sử dụng các công nghệ hiện đại và phổ biến:

| Thành phần | Công nghệ / Thư viện | Vai trò trong hệ thống |
|:---|:---|:---|
| **Backend Core** | `Python 3.10+`, `Flask` | Xử lý logic nghiệp vụ, routing, API |
| **Authentication**| `Flask-Login`, `Werkzeug` | Quản lý session, mã hóa mật khẩu, phân quyền |
| **Database ORM** | `SQLAlchemy` | Giao tiếp cơ sở dữ liệu |
| **Database** | `SQLite` | Cơ sở dữ liệu quan hệ (dễ dàng deploy local) |
| **Frontend** | `HTML5`, `Bootstrap 5`, `Jinja2`, `Vanilla JS` | Giao diện người dùng responsive, rendering view |
| **AI / Data Science**| `pandas`, `scikit-learn` | Tiền xử lý văn bản, thuật toán gợi ý tìm kiếm |

---

## 🚀 Hướng dẫn Cài đặt & Chạy dự án

### Yêu cầu hệ thống (Prerequisites)
- [Python 3.10](https://www.python.org/downloads/) trở lên
- Trình quản lý gói `pip`
- Git

### Các bước cài đặt

**Bước 1: Clone repository**
```bash
git clone https://github.com/<your-org>/ROVVA.git
cd ROVVA
```

**Bước 2: Khởi tạo và kích hoạt môi trường ảo (Virtual Environment)**
```bash
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate

# Kích hoạt trên macOS / Linux:
source venv/bin/activate
```

**Bước 3: Cài đặt các thư viện cần thiết**
```bash
pip install -r requirements.txt
```

**Bước 4: Khởi tạo cơ sở dữ liệu mẫu (Seed Data)**
Lệnh này sẽ tạo cấu trúc bảng, reset dữ liệu cũ (nếu có) và thêm các dữ liệu mẫu (homestay, users, booking...)
```bash
python -m flask --app run seed
```

**Bước 5: Khởi chạy server**
```bash
python run.py
```
> 🎉 **Thành công!** Truy cập hệ thống tại: [http://127.0.0.1:5000](http://127.0.0.1:5000)

---

## 🔑 Tài khoản Demo (Seed Data)

Sử dụng các tài khoản sau để trải nghiệm các tính năng của từng vai trò:

| Vai trò | Email đăng nhập | Mật khẩu | Tính năng chính |
|:---|:---|:---|:---|
| 🧑‍💻 **Customer** | `1@ss` | `1` | Tìm kiếm, Smart Match, Đặt phòng |
| 🏠 **Host** | `van.quangia@rova.vn` | `password123` | Host Dashboard, Copilot AI |
| 🛡️ **Admin** | `admin@rova.vn` | `admin123` | Quản trị hệ thống tổng thể |

---

## 🗺️ Các Endpoint (Routes) Chính

| Chức năng | Đường dẫn (URL) | Mô tả |
|:---|:---|:---|
| **Trang chủ** | `/` | Landing page của hệ thống |
| **Đăng nhập** | `/login` | Cổng xác thực người dùng |
| **Customer Hub** | `/customer/` | Trang quản lý cá nhân của khách |
| **Tìm kiếm thường**| `/customer/search` | Tìm phòng theo bộ lọc cơ bản |
| **Smart Match** | `/customer/smart-search` | Tìm phòng bằng ngôn ngữ tự nhiên |
| **Host Hub** | `/host/` | Bảng điều khiển của Chủ nhà |
| **Host Copilot** | `/host/copilot/` | Công cụ phân tích và trợ lý AI |
| **Admin Hub** | `/admin/` | Bảng điều khiển của Quản trị viên |

---

## 📂 Cấu trúc mã nguồn (Project Structure)

```text
ROVVA/
├── backend/
│   └── app/               # Logic chính của hệ thống
│       ├── models/        # Định nghĩa các thực thể CSDL (SQLAlchemy)
│       ├── routes/        # Định tuyến các endpoints
│       ├── services/      # Chứa thuật toán xử lý (Smart Match, Copilot)
│       └── seed.py        # Kịch bản khởi tạo dữ liệu mẫu
├── frontend/              # Giao diện người dùng
│   ├── static/            # CSS, JavaScript, Images
│   └── templates/         # Jinja2 HTML templates
├── docs/                  # Tài liệu dự án (SRS, ERD, Kiến trúc)
├── scripts/               # Các script tiện ích (vd: xử lý ảnh demo)
├── tests/                 # Unit tests và Integration tests
├── instance/              # Thư mục chứa file SQLite (tạo ra khi chạy)
├── requirements.txt       # Danh sách dependencies
└── run.py                 # Điểm khởi chạy (Entry point) của ứng dụng
```

---

## 📚 Tài liệu tham khảo dự án

Để hiểu rõ hơn về cách thiết kế và vận hành, vui lòng tham khảo các tài liệu phân tích trong thư mục `docs/`:

- 📑 [**SRS (Software Requirements Specification)**](docs/SRS.md) — Đặc tả yêu cầu kỹ thuật chi tiết.
- 🗄️ [**ERD (Entity-Relationship Diagram)**](docs/ERD.md) — Sơ đồ quan hệ cơ sở dữ liệu.
- 🏗️ [**Architecture**](docs/ARCHITECTURE.md) — Sơ đồ kiến trúc tổng thể của hệ thống.
- 📈 [**Báo cáo tiến độ**](docs/BAO_CAO_SRS.md) — Đánh giá tiến độ hoàn thiện so với tài liệu SRS.

---

## 📄 Bản quyền (License)

Dự án này được phát triển độc quyền nhằm mục đích học tập, nghiên cứu và thử nghiệm công nghệ. 
