# ROVVA — Smart Stay Platform

Website đặt phòng homestay/khách sạn cho môn học (Flask + Bootstrap + SQLite).  
Hỗ trợ 3 vai trò: **Guest/Customer**, **Host**, **Admin**.  
Killer feature: **Smart Match** — tìm phòng bằng câu tiếng Việt tự nhiên (TF-IDF + AI ranking).

---

## Yêu cầu hệ thống

- **Python 3.10+** (khuyến nghị 3.12)
- **Git**
- Trình duyệt Chrome / Edge / Firefox

---

## Cài đặt nhanh (lần đầu)

### 1. Clone repository

```powershell
git clone <URL-repo-cua-team>.git
cd ROVVA
```

### 2. Tạo virtual environment (khuyến nghị)

```powershell
py -m venv venv
.\venv\Scripts\Activate.ps1
```

Nếu PowerShell chặn script:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

### 3. Cài dependencies

```powershell
pip install -r requirements.txt
```

### 4. Khởi tạo database + dữ liệu demo

```powershell
py -m flask --app run seed
```

Lệnh này **xóa và tạo lại** toàn bộ DB, seed 12 cơ sở lưu trú, booking mẫu, tài khoản demo.

### 5. Chạy server

```powershell
py run.py
```

Mở trình duyệt: **http://127.0.0.1:5000**

---

## Tài khoản demo

| Vai trò | Email | Mật khẩu |
|---------|-------|----------|
| Khách hàng | `1@ss` | `1` |
| Host | `van.quangia@rova.vn` | `password123` |
| Admin | `admin@rova.vn` | `admin123` |

---

## URL quan trọng

| Trang | URL |
|-------|-----|
| Trang chủ (guest) | http://127.0.0.1:5000/ |
| Trang chủ customer | http://127.0.0.1:5000/customer/ |
| Đăng nhập | http://127.0.0.1:5000/login |
| Đăng ký | http://127.0.0.1:5000/register |
| Tìm kiếm filter | http://127.0.0.1:5000/customer/search |
| Smart Match (AI) | http://127.0.0.1:5000/customer/smart-search?q=homestay+Đà+Lạt+có+hồ+bơi |
| Khu vực Host | http://127.0.0.1:5000/host/ |
| Khu vực Admin | http://127.0.0.1:5000/admin/ |

---

## Cấu trúc thư mục

```
ROVVA/
├── backend/app/          # Flask app, models, routes, services
│   ├── models/         # SQLAlchemy models
│   ├── routes/         # Blueprints (customer, host, admin, auth)
│   ├── services/       # Smart Match AI
│   ├── utils/          # media helper (ảnh theo ID)
│   └── seed.py         # Dữ liệu demo
├── frontend/
│   ├── templates/      # Jinja2 HTML
│   └── static/         # CSS, JS, images
├── instance/           # SQLite DB (tự tạo khi chạy)
├── docs/               # Tài liệu hướng dẫn
├── UI_FIGMA/           # Thiết kế Figma tham chiếu
├── run.py              # Entry point
├── requirements.txt
├── PLAINING.md         # Báo cáo tiến độ & roadmap
└── SRS_Homestay_Project.md
```

---

## Bổ sung ảnh demo (cho team)

Xem chi tiết: **[docs/HUONG_DAN_ANH_DEMO.md](docs/HUONG_DAN_ANH_DEMO.md)**

Tóm tắt — thả ảnh vào:

```
frontend/static/customer/images/accommodations/<acc_id>/cover.jpg
frontend/static/customer/images/accommodations/<acc_id>/gallery/1.jpg … 5.jpg
frontend/static/customer/images/accommodations/<acc_id>/rooms/<room_id>.jpg
```

Không có ảnh → hệ thống hiển thị placeholder SVG tự động.

---

## Lệnh hữu ích

```powershell
# Chạy app
py run.py

# Reset + seed lại database
py -m flask --app run seed

# Test Smart Match (CLI)
py -m backend.app.services.smart_match "phòng cho 2 người có hồ bơi"

# Tra ID cơ sở lưu trú / phòng (để đặt ảnh)
py -c "from backend.app import create_app; from backend.app.models import Accommodation; app=create_app(); ctx=app.app_context(); ctx.push(); [print(a.id, a.name) for a in Accommodation.query.all()]"
```

---

## Push lên GitHub (quy trình cho team)

### Lần đầu — tạo repo & push

```powershell
# 1. Khởi tạo git (nếu chưa có)
git init

# 2. Kiểm tra file sẽ commit (KHÔNG commit .env, venv)
git status

# 3. Add file
git add .
git add frontend/static/customer/images/accommodations/

# 4. Commit
git commit -m "Initial commit: ROVVA homestay platform"

# 5. Tạo repo trên GitHub (web), rồi:
git remote add origin https://github.com/<team>/<repo>.git
git branch -M main
git push -u origin main
```

### Các lần sau — làm việc nhóm

```powershell
# Luôn pull trước khi code
git pull origin main

# Tạo nhánh cho tính năng (khuyến nghị)
git checkout -b feature/ten-tinh-nang

# ... code, test ...

git add .
git commit -m "Mô tả ngắn thay đổi (tiếng Việt hoặc Anh)"
git push -u origin feature/ten-tinh-nang
```

Sau đó tạo **Pull Request** trên GitHub để review trước khi merge vào `main`.

### Quy tắc commit (team)

- **Commit message** rõ ràng: `Thêm ảnh demo CSLT #1-#4`, `Sửa route đăng nhập guest`
- **Không commit:** `venv/`, `__pycache__/`, `.env`, file `.db` lớn (dùng `flask seed` để tái tạo)
- **Nên commit:** code, template, ảnh demo đã nén, tài liệu `docs/`

### Xử lý conflict cơ bản

```powershell
git pull origin main
# Nếu conflict → mở file, sửa phần <<<<<<< ======= >>>>>>>
git add .
git commit -m "Resolve merge conflict"
git push
```

---

## Báo cáo tiến độ dự án

Xem file **[PLAINING.md](PLAINING.md)** — bảng đối chiếu SRS, checklist đã làm/chưa làm, roadmap.

---

## Tech stack

| Layer | Công nghệ |
|-------|-----------|
| Backend | Python, Flask, Flask-Login, SQLAlchemy |
| Database | SQLite |
| Frontend | HTML, Bootstrap 5, Jinja2, JavaScript |
| AI / Data | pandas, scikit-learn (Smart Match) |

---

## License & môn học

Dự án phục vụ mục đích học tập — HK3 ROVVA Homestay (5 thành viên, 7 ngày).

---

## Liên hệ nội bộ team

- **Backend / DB:** xem `backend/app/`
- **UI Customer:** `frontend/templates/customer/`
- **UI Admin:** `frontend/templates/admin/`
- **UI Host:** `frontend/templates/host/`
- **Ảnh demo:** `docs/HUONG_DAN_ANH_DEMO.md`
