# Báo cáo tiến độ — đối chiếu SRS

> Đối chiếu `docs/SRS.md` với code thực tế ROVVA.  
> **Cập nhật: 10/07/2026**

---

## Tóm tắt

| Hạng mục | Trạng thái |
|----------|------------|
| Luồng Customer (tìm → xem → đặt → thanh toán) | ✅ End-to-end |
| Smart Match (TF-IDF + cosine similarity) | ✅ |
| Customer SSR + dữ liệu thật | ✅ |
| Ảnh demo CSLT (104 ảnh, 12 CSLT) | ✅ |
| Admin (dashboard + 10 module) | ✅ |
| Host (CSLT, booking, payment, dispute, message, promotion) | ✅ |
| **Host Copilot** (persona, maintenance radar, revenue advisor) | ✅ MVP |
| Auth email thật / payment gateway thật | 🔴 |
| Booking lifecycle đầy đủ (hủy, check-in/out) | 🔴 |

**Ước lượng hoàn thành SRS:** ~**75–80%** chức năng cốt lõi; đủ demo môn học + báo cáo.

---

## Killer features (ngoài SRS)

| Feature | Mô tả | Trạng thái |
|---------|-------|------------|
| Smart Match | Tìm phòng bằng câu tiếng Việt tự nhiên | ✅ |
| Host Copilot | Guest persona, maintenance radar, revenue advisor | ✅ |
| Media theo ID | Ảnh CSLT/phòng/avatar + placeholder SVG | ✅ |

---

## 1. Yêu cầu chức năng (FR)

Chú thích: ✅ Hoàn thành · 🟡 Một phần · 🔴 Chưa

### 2.1 Quản lý tài khoản

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-A-01 | Đăng ký tài khoản | ✅ | Validate email unique, confirm password |
| FR-A-02 | Xác thực email | 🟡 | Token + route; chưa gửi email SMTP thật |
| FR-A-03 | Đăng nhập + phân quyền | 🟡 | Redirect guest/host/admin OK; một số host route chưa siết RBAC |
| FR-A-04 | Quên mật khẩu | 🟡 | Logic token có; thiếu template forgot/reset |
| FR-A-05 | Cập nhật thông tin | ✅ | Customer profile POST; Host profile; avatar qua `avatar_url` |
| FR-A-06 | Đăng xuất | ✅ | `/logout` |

### 2.2 Đăng ký cho thuê (Host)

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-H-01 | Đăng ký Host | 🟡 | Route `become-host`; upload mock |
| FR-H-02 | Kiểm duyệt hồ sơ | ✅ | Admin approve/reject |
| FR-H-03 | Cập nhật Role Host | ✅ | Admin approve → `role=host` |
| FR-H-04 | Quản lý thông tin Host | ✅ | `host/profile` + edit |

### 2.3 Quản lý nơi cư trú

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-R-01 | Đăng phòng mới | ✅ | CRUD accommodation + room |
| FR-R-02 | Cập nhật phòng | ✅ | Edit form |
| FR-R-03 | Dynamic pricing | 🔴 | UI pricing có; chưa lưu giá theo ngày |
| FR-R-04 | Quản lý trạng thái | ✅ | active/pending/paused/draft |
| FR-R-05 | Quản lý hình ảnh | 🟡 | Ảnh theo ID + script fill; chưa upload qua UI |
| FR-R-06 | Đồng bộ lịch | 🟡 | Overlap check khi đặt; chưa calendar block |

### 2.4 Đặt phòng

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-B-01 | Tìm kiếm phòng | ✅ | Filter SSR + Smart Match AI |
| FR-B-02 | Xem chi tiết | ✅ | Mosaic ảnh, modal phòng, reviews |
| FR-B-03 | Giữ phòng tạm | ✅ | HOLDING 15 phút |
| FR-B-04 | Tạo Booking | ✅ | POST → checkout → confirmed |
| FR-B-05 | Hủy Booking | 🔴 | UI có; chưa route hủy + release lịch |
| FR-B-06 | Thông báo Booking | 🔴 | Chưa email/push notification |

### 2.5 Thanh toán

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-P-01 | Thanh toán Online | ✅ (mock) | Mock gateway + success page |
| FR-P-02 | Thanh toán Tiền mặt | ✅ (mock) | Checkout cash |
| FR-P-03 | Verify giao dịch | 🟡 | Callback giả lập |
| FR-P-04 | Cập nhật trạng thái | ✅ | `payment_status`, commission, host payout |
| FR-P-05 | Lịch sử giao dịch | ✅ | Admin payments; Host payment (filter theo host); Customer wallet |

### 2.6 Quản lý lưu trú

| ID | Yêu cầu | Trạng thái | Ghi chú |
|----|---------|------------|---------|
| FR-S-01 | Check-in | 🔴 | Chưa route |
| FR-S-02 | Check-out | 🔴 | Chưa route |
| FR-S-03 | Tranh chấp | 🟡 | Host + Admin resolve; Customer mở ticket chưa |
| FR-S-04 | Đánh giá | 🟡 | Hiển thị + seed; chưa route tạo review |
| FR-S-05 | Trạng thái lưu trú | 🔴 | Chưa luồng `completed` tự động |

---

## 2. Yêu cầu phi chức năng (NFR)

| ID | Hạng mục | Trạng thái | Ghi chú |
|----|----------|------------|---------|
| NFR-01 | Hiệu năng < 3s | ✅ (dev) | SQLite, dataset nhỏ |
| NFR-02 | 100 CCU | 🔴 | Chưa load test |
| NFR-03 | Bảo mật | 🟡 | Password hash ✅; HTTPS chưa |
| NFR-04 | RBAC 3 role | 🟡 | Admin `@login_required`; host đã cải thiện (booking, payment, copilot) |
| NFR-05 | Không double booking | 🟡 | Overlap check; chưa DB lock/transaction |
| NFR-06 | Chịu lỗi giao dịch | 🟡 | Mock cơ bản |
| NFR-07 | Backup | 🔴 | Chưa tự động |
| NFR-08 | Mở rộng | ✅ | Blueprint + services tách module |
| NFR-09 | Responsive UI | ✅ | Bootstrap 5 |
| NFR-10 | Cấu trúc module | ✅ | Factory pattern, blueprints |
| NFR-11 | Uptime 99% | 🔴 | Chưa deploy production |
| NFR-12 | Usability | 🟡 | Flash messages; một số trang còn mock |

---

## 3. Đã hoàn thành (checklist)

### Nền tảng
- [x] Flask application factory, SQLAlchemy, Flask-Login
- [x] 12 bảng DB (xem `docs/ERD.md`)
- [x] Seed demo: users, 12 CSLT, 32 phòng, 14 booking, review, dispute, promotion, withdrawal
- [x] Routing: `/` → guest, `/login`, `/customer/`, `/host/`, `/admin/`

### Customer
- [x] Trang chủ guest/member SSR
- [x] Tìm kiếm filter `/customer/search`
- [x] Smart Match `/customer/smart-search`
- [x] Chi tiết CSLT, checkout, thanh toán mock, success
- [x] Tài khoản: profile, trips, wallet, favorites, reviews, tier, security
- [x] Become host registration

### Host
- [x] Dashboard tổng quan
- [x] CRUD CSLT + phòng + khuyến mãi
- [x] Quản lý booking (filter theo host)
- [x] Thanh toán & rút tiền (logic đúng, filter host)
- [x] Tranh chấp, tin nhắn
- [x] Ảnh `cover_url` / `image_url` / `avatar_url`
- [x] **Host Copilot**: persona, maintenance radar, revenue advisor

### Admin
- [x] Dashboard thống kê
- [x] Quản lý customers, hosts (duyệt), accommodations, rooms
- [x] Bookings, disputes (resolve), payments, promotions, admins

### AI / Data
- [x] `smart_match.py` — TF-IDF + cosine + rating blend
- [x] `host_copilot/` — rule engine persona, maintenance, revenue

### Media
- [x] 104 ảnh demo cho 12 CSLT
- [x] Placeholder SVG fallback
- [x] Script `scripts/fill_accommodation_images.py`

---

## 4. Chưa hoàn thành / còn thiếu

### Ưu tiên cao (nếu bổ sung sau demo)
1. Route **hủy booking** + giải phóng lịch phòng
2. Route **tạo review** sau chuyến đi `completed`
3. **Check-in / Check-out** + cập nhật status booking
4. Template **forgot/reset password**
5. Siết RBAC toàn bộ host routes (message, report còn mock)

### Ưu tiên thấp / ngoài phạm vi môn học
6. Gửi email SMTP thật (verify, booking confirm)
7. Payment gateway thật (VNPay, MoMo…)
8. Dynamic pricing theo ngày
9. Upload ảnh qua UI Host
10. Host report thay mock bằng Chart.js + data thật
11. Load test 100 CCU, backup tự động, deploy HTTPS

---

## 5. Thống kê nhanh

| Metric | Giá trị |
|--------|---------|
| Models (bảng) | 12 |
| Blueprints | auth, customer, host (9 module), admin |
| CSLT demo | 12 |
| Phòng demo | 32 |
| Ảnh demo | 104 JPG |
| FR hoàn thành / tổng (ước lượng) | ~28 / 36 (~78%) |
| NFR hoàn thành / tổng (ước lượng) | ~5 / 12 (~42%) |

---

## 6. Tài khoản demo

| Vai trò | Email | Mật khẩu | Sau login |
|---------|-------|----------|-----------|
| Customer | `1@ss` | `1` | `/customer/` |
| Host | `van.quangia@rova.vn` | `password123` | `/host/` |
| Admin | `admin@rova.vn` | `admin123` | `/admin/` |
| Host chờ duyệt | `host.pending@rova.vn` | `123456` | Duyệt tại Admin |

---

## 7. Tài liệu liên quan

- [SRS gốc](SRS.md)
- [ERD](ERD.md)
- [Kiến trúc hệ thống](ARCHITECTURE.md)
- [Hướng dẫn ảnh demo](HUONG_DAN_ANH_DEMO.md)
- [README](../README.md)
