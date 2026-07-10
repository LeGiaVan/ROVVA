# KẾ HOẠCH & BÁO CÁO TIẾN ĐỘ DỰ ÁN ROVVA HOMESTAY

> Tài liệu sống (living doc) — đối chiếu SRS với code thực tế và theo dõi tiến độ.  
> **Cập nhật gần nhất: 09/07/2026** (sau phiên hoàn thiện Customer SSR + Admin).

---

## TÓM TẮT EXECUTIVE

| Hạng mục | Trạng thái |
|----------|------------|
| **Luồng cốt lõi Customer** (tìm → xem → đặt → thanh toán) | ✅ Chạy end-to-end |
| **Killer Feature Smart Match (AI)** | ✅ Hoàn thành |
| **Customer SSR + dữ liệu thật** | ✅ Hoàn thành (phiên 09/07) |
| **Khu vực Admin** | ✅ Backend + UI cơ bản |
| **Ảnh demo** | 🟡 Cơ chế sẵn, team đang fill ảnh |
| **Host CRUD** | ✅ Khá đầy đủ |
| **Auth email thật / gateway thật** | 🔴 Chưa |
| **Booking lifecycle đầy đủ** (hủy, check-in/out) | 🔴 Chưa |

**Ước lượng tiến độ SRS:** ~**65–70%** chức năng cốt lõi; phù hợp demo môn học nếu bổ sung ảnh + rehearsal luồng chính.

---

## 0. NHẬT KÝ CẬP NHẬT

### Phiên 09/07/2026 — Customer SSR Overhaul (theo Figma)

#### ✅ Cụm 1 — Nền tảng ảnh + dữ liệu
- Quy ước thư mục ảnh theo ID: `frontend/static/customer/images/accommodations/<acc_id>/...`
- Helper `resolve_media()` + placeholder SVG (`accommodation`, `room`, `avatar`)
- Property model: `Accommodation.cover_url`, `gallery_urls`, `min_price`, `top_features`; `Room.image_url`; `User.avatar_url`
- Sửa `seed.py`: status booking dùng hằng số model, `guest_id` cho khách mẫu, seed ví xu + yêu thích
- Sửa mojibake filter type trang chủ; render CSLT thật cho guest/member

#### ✅ Cụm 2 — Tìm kiếm filter (SSR)
- Route `GET /customer/search` (địa điểm, giá, loại hình, số khách, tiện ích, sort)
- Trang `search-results.html` + nối form `search-bar.html`

#### ✅ Cụm 3 — Chi tiết + thanh toán
- `detail.html`: mosaic ảnh, tiện ích/dịch vụ, host, map, reviews, modal chi tiết phòng
- `checkout.html` nâng cấp: thông tin khách, dịch vụ, mã giảm, đổi xu, chi tiết giá
- Trang `payment/success.html`; route `customer_booking.success`

#### ✅ Cụm 4 — Tài khoản Customer (SSR)
- Sidebar Jinja `_sidebar.html` + active state
- Routes: profile (POST), trips (tabs), wallet, favorites, reviews, security, tier
- Cột User: `gender`, `birthday`, `city`

#### ✅ Cụm 5 — Guest + routing
- Trang guest dùng chung route SSR (`/customer/`)
- Route gốc `/` → trang guest (không còn trang login)
- Login `/login`, Register `/register`; sửa link header guest
- `app.js` tối giản; flash messages trong `base.html`

#### ✅ Admin (phiên cuối 09/07)
- Seed tài khoản admin + host pending
- UI Admin: sidebar Figma, dashboard, 10 module (customers, hosts, accommodations, rooms, bookings, disputes, payments, promotions, admins)
- Redirect admin sau login → `/admin/`

### Phiên trước — Luồng booking + Smart Match
- Form đặt phòng POST → `HOLDING` 15' → checkout → mock gateway → `CONFIRMED`
- `smart_match.py`: TF-IDF + cosine similarity + rating blend + lý do gợi ý
- Route `/customer/smart-search`; UI `smart-results.html`

---

## 1. BẢNG ĐÁNH GIÁ TIẾN ĐỘ (cập nhật)

Chú thích: ✅ Hoàn thành · 🟡 Một phần · 🔴 Chưa bắt đầu

### A. Yêu cầu Chức năng (FR)

#### 2.1 Quản lý tài khoản
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-A-01 | Đăng ký tài khoản | ✅ | Validate email unique, confirm password |
| FR-A-02 | Xác thực email | 🟡 | Token + route có; **chưa gửi email thật** (mock verify page) |
| FR-A-03 | Đăng nhập + phân quyền | 🟡 | Login/redirect guest/host/admin OK; host routes vẫn thiếu siết RBAC |
| FR-A-04 | Quên mật khẩu | 🟡 | Logic token có; **thiếu template** forgot/reset |
| FR-A-05 | Cập nhật thông tin | 🟡 | **Customer profile POST OK**; Host profile OK; avatar chưa upload file |
| FR-A-06 | Đăng xuất | ✅ | `/logout` chuẩn |

#### 2.2 Đăng ký cho thuê (Host)
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-H-01 | Đăng ký Host | 🟡 | Route `become-host` có; upload mock |
| FR-H-02 | Kiểm duyệt hồ sơ | ✅ | **Admin UI + approve/reject Host** |
| FR-H-03 | Cập nhật Role Host | ✅ | Admin approve → `role=host` |
| FR-H-04 | Quản lý thông tin Host | ✅ | `host/profile` + edit |

#### 2.3 Quản lý nơi cư trú
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-R-01 | Đăng phòng mới | ✅ | CRUD create (hardcode host_id còn tồn tại) |
| FR-R-02 | Cập nhật phòng | ✅ | Edit accommodation + room |
| FR-R-03 | Dynamic pricing | 🔴 | UI có, chưa route lưu giá theo ngày |
| FR-R-04 | Quản lý trạng thái | ✅ | Model + form |
| FR-R-05 | Quản lý hình ảnh | 🟡 | **Cơ chế thả ảnh theo ID + placeholder**; chưa upload qua UI |
| FR-R-06 | Đồng bộ lịch | 🟡 | Overlap check khi đặt; chưa calendar block |

#### 2.4 Đặt phòng
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-B-01 | Tìm kiếm phòng | ✅ | **Smart Match AI** + **filter SSR** `/customer/search` |
| FR-B-02 | Xem chi tiết | ✅ | Mosaic, modal phòng, reviews, map |
| FR-B-03 | Giữ phòng tạm | ✅ | HOLDING 15 phút |
| FR-B-04 | Tạo Booking | ✅ | End-to-end |
| FR-B-05 | Hủy Booking | 🔴 | UI có, **chưa route hủy** |
| FR-B-06 | Thông báo Booking | 🔴 | Chưa email/notification |

#### 2.5 Thanh toán
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-P-01 | Thanh toán Online | ✅ (mock) | Mock gateway + success page |
| FR-P-02 | Thanh toán Tiền mặt | ✅ (mock) | Checkout cash → confirmed |
| FR-P-03 | Verify giao dịch | 🟡 | Callback giả lập |
| FR-P-04 | Cập nhật trạng thái | 🟡 | `payment_status` cơ bản |
| FR-P-05 | Lịch sử giao dịch | 🟡 | Admin payments + Host; Customer wallet OK |

#### 2.6 Quản lý lưu trú
| ID | Tính năng | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| FR-S-01 | Check-in | 🔴 | Chưa route |
| FR-S-02 | Check-out | 🔴 | Chưa route |
| FR-S-03 | Tranh chấp | 🟡 | Host + **Admin resolve**; Customer mở ticket chưa |
| FR-S-04 | Đánh giá | 🟡 | Hiển thị + seed; **chưa route tạo review** |
| FR-S-05 | Trạng thái lưu trú | 🔴 | Chưa luồng completed tự động |

### B. Yêu cầu Phi chức năng (NFR)
| ID | Hạng mục | Trạng thái | Ghi chú |
| :--- | :--- | :--- | :--- |
| NFR-01 | Hiệu năng < 3s | ✅ (dev) | SQLite + data nhỏ |
| NFR-02 | 100 CCU | 🔴 | Chưa load test |
| NFR-03 | Bảo mật | 🟡 | Hash password ✅; HTTPS chưa |
| NFR-04 | RBAC 3 role | 🟡 | Admin decorator ✅; host routes hở |
| NFR-05 | Không double booking | 🟡 | Overlap check; chưa DB lock |
| NFR-06 | Chịu lỗi giao dịch | 🟡 | Mock cơ bản |
| NFR-07 | Backup | 🔴 | Chưa |
| NFR-08 | Mở rộng | 🟡 | Blueprint tốt |
| NFR-09 | Responsive UI | ✅ | Bootstrap 5 + CSS Figma |
| NFR-10 | Cấu trúc module | ✅ | Factory + blueprints + services |
| NFR-11 | Uptime 99% | 🔴 | Chưa deploy |
| NFR-12 | Usability | 🟡 | Flash messages; chưa đồng bộ toàn hệ |

---

## 2. KILLER FEATURE — Smart Match ✅

| Thành phần | Trạng thái |
|------------|------------|
| Core `smart_match.py` (TF-IDF + cosine + rating) | ✅ |
| Route `/customer/smart-search` | ✅ |
| UI kết quả (score, rating, reason chips) | ✅ |
| Thư viện pandas, scikit-learn, numpy | ✅ |

**Demo nhanh:**
```bash
py -m backend.app.services.smart_match "homestay Đà Lạt cho 4 người có hồ bơi"
```

---

## 3. ĐÃ LÀM ĐƯỢC (checklist tổng hợp)

- [x] Kiến trúc Flask (application factory, blueprints, SQLAlchemy)
- [x] Seed demo: 12 CSLT, 32 phòng, booking, review, dispute, promotion
- [x] Auth: login, register, verify mock, brute-force lock
- [x] Customer: trang chủ guest/member SSR, search filter, detail, booking, checkout, success
- [x] Smart Match AI
- [x] Account customer: profile, trips, wallet, favorites, reviews list, tier, security UI
- [x] Admin: dashboard + duyệt host/CSLT + quản lý booking/dispute/payment
- [x] Host: accommodation CRUD, booking, message, dispute, payment, promotion
- [x] Cơ chế ảnh theo ID + placeholder
- [x] Routing: `/` = guest, `/login`, `/customer/`, `/admin/`

---

## 4. CHƯA LÀM / CÒN THIẾU (ưu tiên)

### P0 — Cần trước buổi demo
1. **Fill ảnh demo** theo `docs/HUONG_DAN_ANH_DEMO.md`
2. **Rehearsal luồng:** guest search → detail → login → book → pay → trips
3. Template **forgot/reset password** (nếu giảng viên hỏi)

### P1 — Hoàn thiện SRS
4. Route **hủy booking** + release lịch
5. Route **tạo review** sau chuyên đi hoàn thành
6. **Check-in / Check-out** + chuyển status `completed`
7. Siết **RBAC host** (`@host_required`, bỏ `host_id=1` hardcode)

### P2 — Nâng cao (nếu còn thời gian)
8. Gửi email thật (Flask-Mail)
9. Gateway thanh toán thật
10. Insight Dashboard Host (Pandas + Chart.js) — xem mục 5
11. Dynamic pricing theo ngày
12. Upload ảnh qua UI Host

---

## 5. ĐỀ XUẤT DỰ PHÒNG — Insight Dashboard Host

Thay mock tại `host/report/index.html` bằng phân tích thật từ Booking/Review: doanh thu theo tháng, dự báo Linear Regression, Chart.js.

---

## 6. TÀI KHOẢN DEMO

| Vai trò | Email | Mật khẩu | URL sau login |
|---------|-------|----------|---------------|
| Guest / Customer | `1@ss` | `1` | `/customer/` (member) |
| Host | `van.quangia@rova.vn` | `password123` | `/host/` |
| Admin | `admin@rova.vn` | `admin123` | `/admin/` |
| Host chờ duyệt | `host.pending@rova.vn` | `123456` | — (duyệt tại Admin) |

---

## 7. VIỆC TIẾP THEO (roadmap ngắn)

| Tuần | Việc |
|------|------|
| Tuần 1 | Fill ảnh + rehearsal demo + fix bug UI nhỏ |
| Tuần 2 | Hủy booking + review + RBAC host |
| Tuần 3 | Check-in/out + polish Admin/Host |
| Tuần 4 | Deploy (optional) + slide báo cáo |

---

## 8. TÀI LIỆU LIÊN QUAN

- `SRS_Homestay_Project.md` — đặc tả yêu cầu gốc
- `SYSTEM_ARCHITECTURE.md` — kiến trúc hệ thống
- `docs/HUONG_DAN_ANH_DEMO.md` — hướng dẫn team bổ sung ảnh
- `README.md` — cài đặt & push GitHub
