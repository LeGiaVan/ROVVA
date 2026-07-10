# ROVVA — Smart Stay Platform

Nền tảng đặt phòng homestay và khách sạn, xây dựng với Flask và Server-Side Rendering. Hệ thống hỗ trợ ba vai trò: **Customer**, **Host** và **Admin**.

## Tính năng nổi bật

- **Smart Match** — tìm phòng bằng mô tả tiếng Việt tự nhiên (TF-IDF + cosine similarity)
- **Host Copilot** — trợ lý vận hành: phân tích persona khách, radar bảo trì, gợi ý doanh thu
- **Luồng đặt phòng** — tìm kiếm, xem chi tiết, giữ phòng, thanh toán mock, xác nhận booking
- **Quản lý đa vai trò** — customer account, host dashboard, admin panel
- **Media theo ID** — ảnh CSLT/phòng/avatar với fallback placeholder

## Tech stack

| Layer | Công nghệ |
|-------|-----------|
| Backend | Python, Flask, Flask-Login, SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, Bootstrap 5, Jinja2, JavaScript |
| AI / Data | pandas, scikit-learn |

## Yêu cầu

- Python 3.10+
- pip

## Cài đặt & chạy

```bash
git clone https://github.com/<your-org>/ROVVA.git
cd ROVVA

python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt
python -m flask --app run seed
python run.py
```

Truy cập: **http://127.0.0.1:5000**

> `flask seed` sẽ reset và tạo lại database cùng dữ liệu demo.

## Tài khoản demo

| Vai trò | Email | Mật khẩu |
|---------|-------|----------|
| Customer | `1@ss` | `1` |
| Host | `van.quangia@rova.vn` | `password123` |
| Admin | `admin@rova.vn` | `admin123` |

## Các route chính

| Trang | URL |
|-------|-----|
| Trang chủ | `/` |
| Customer | `/customer/` |
| Tìm kiếm | `/customer/search` |
| Smart Match | `/customer/smart-search` |
| Host | `/host/` |
| Host Copilot | `/host/copilot/` |
| Admin | `/admin/` |
| Đăng nhập | `/login` |

## Cấu trúc dự án

```
ROVVA/
├── backend/app/       # Models, routes, services, seed
├── frontend/          # Templates Jinja2 + static assets
├── docs/              # SRS, ERD, architecture, báo cáo
├── scripts/           # Tiện ích bổ sung ảnh demo
├── tests/
├── instance/          # SQLite database (local)
└── run.py             # Entry point
```

## Tài liệu

- [SRS](docs/SRS.md) — đặc tả yêu cầu
- [ERD](docs/ERD.md) — sơ đồ quan hệ database
- [Architecture](docs/ARCHITECTURE.md) — kiến trúc hệ thống
- [Báo cáo tiến độ](docs/BAO_CAO_SRS.md) — đối chiếu với SRS

## License

Dự án phục vụ mục đích học tập.
