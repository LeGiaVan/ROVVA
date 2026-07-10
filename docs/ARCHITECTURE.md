# Kiến trúc hệ thống — ROVVA

**Tên dự án:** ROVVA Smart Stay Platform  
**Miền nghiệp vụ:** Đặt phòng homestay / khách sạn đa vai trò (Customer, Host, Admin)  
**Kiến trúc:** Server-Side Rendering (Flask + Jinja2 + SQLite)

---

## Technology stack

| Thành phần | Công nghệ |
|------------|-----------|
| Backend | Python 3.10+, Flask 3, Flask-Login, Flask-SQLAlchemy |
| Database | SQLite (`instance/rova_host.db`) |
| Frontend | HTML5, Bootstrap 5, Jinja2, Vanilla JS |
| AI / Analytics | pandas, scikit-learn (`smart_match`, `host_copilot`) |

---

## Cấu trúc repository

```text
ROVVA/
├── backend/app/
│   ├── __init__.py          # Application factory
│   ├── config.py            # Dev/Prod config
│   ├── extensions.py        # db, login_manager
│   ├── models/              # 12 ORM models
│   ├── routes/
│   │   ├── auth/            # Login, register, logout
│   │   ├── customer/        # Search, booking, account
│   │   ├── host/            # CSLT, booking, payment, copilot…
│   │   └── admin/           # Quản trị hệ thống
│   ├── services/
│   │   ├── smart_match.py   # TF-IDF room matching
│   │   └── host_copilot/    # Persona, maintenance, revenue
│   ├── utils/media.py       # Ảnh theo ID + placeholder
│   └── seed.py              # Dữ liệu demo
├── frontend/
│   ├── templates/           # customer, host, admin, auth
│   └── static/              # CSS, JS, images
├── docs/                    # SRS, ERD, báo cáo, design
├── scripts/                 # fill_accommodation_images.py
├── tests/
├── instance/                # SQLite (gitignored)
└── run.py
```

---

## Blueprints & URL prefix

| Blueprint | Prefix | Vai trò |
|-----------|--------|---------|
| `auth` | `/login`, `/register`, `/logout` | Xác thực |
| `customer` | `/customer/` | Khách hàng |
| `main` (host) | `/host/` | Dashboard host |
| `accommodation` | `/host/accommodation/` | CRUD CSLT |
| `booking` | `/host/booking/` | Quản lý booking |
| `payment` | `/host/payment/` | Thanh toán, rút tiền |
| `copilot` | `/host/copilot/` | Host Copilot |
| `dispute`, `message`, `promotion`, `report` | `/host/...` | Module host |
| `admin` | `/admin/` | Quản trị |

Route gốc `/` redirect theo role: guest → `/customer/`, host → `/host/`, admin → `/admin/`.

---

## Luồng request

```text
HTTP Request
    → Flask router (blueprint)
    → Flask-Login (session → current_user)
    → Route handler (@login_required nếu cần)
    → SQLAlchemy ORM / Service layer
    → render_template() → Jinja2 HTML
    → HTTP Response
```

### Luồng đặt phòng (Customer)

```text
Search / Smart Match → Detail CSLT → POST book
    → Booking HOLDING (15 phút)
    → Checkout → Mock payment
    → Booking CONFIRMED
```

---

## Services layer

### Smart Match (`services/smart_match.py`)
- Đọc rooms + accommodations từ SQLite (Pandas)
- TF-IDF vectorize corpus mô tả phòng
- Cosine similarity + blend rating
- Trả top N phòng kèm `reasons`

### Host Copilot (`services/host_copilot/`)
- `persona.py` — suy luận loại khách từ booking
- `maintenance.py` — quét review/message, phát hiện issue
- `revenue.py` — gợi ý tăng doanh thu từ occupancy
- `context.py` — gom metrics host

---

## Media & static files

Ảnh không lưu trong DB. Quy ước path:

- `customer/images/accommodations/<id>/cover.jpg`
- `customer/images/accommodations/<id>/rooms/<room_id>.jpg`
- `customer/images/avatars/<user_id>.jpg`

Helper `utils/media.py` → `resolve_media()` fallback placeholder SVG.

---

## Database

12 bảng — chi tiết xem [ERD.md](ERD.md).

Seed: `py -m flask --app run seed` (drop + create + insert demo).

Patch demo: `patch_host_payment_demo()` chạy khi app khởi động.

---

## Phân quyền (RBAC)

| Role | Quyền |
|------|-------|
| `guest` / customer | Tìm, đặt, tài khoản |
| `host` | Quản lý CSLT, booking, payment của mình |
| `admin` | Toàn hệ thống, duyệt host/CSLT, resolve dispute |

Trạng thái: một số host routes vẫn cần siết RBAC đầy đủ (report mock, message hardcode).

---

## Triển khai (dev)

```powershell
pip install -r requirements.txt
py -m flask --app run seed
py run.py
```

Production (chưa): cần PostgreSQL, Redis session, HTTPS, WSGI server (gunicorn).

---

## Tài liệu liên quan

- [ERD](ERD.md)
- [SRS](SRS.md)
- [Báo cáo tiến độ](BAO_CAO_SRS.md)
