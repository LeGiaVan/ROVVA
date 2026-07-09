# KẾ HOẠCH & TIẾN ĐỘ DỰ ÁN ROVVA HOMESTAY

> Tài liệu sống (living doc) — đối chiếu SRS với code thực tế và theo dõi tiến độ.
> Cập nhật gần nhất: **09/07/2026**.

**Tóm tắt hiện trạng:** Nền tảng (kiến trúc, DB model, UI Bootstrap) tốt. Trong phiên gần nhất đã **nối xong luồng đặt phòng end-to-end** (detail → giữ chỗ → thanh toán mô phỏng → xác nhận) và **hoàn thành Killer Feature "Smart Match"** (tìm phòng bằng ngôn ngữ tự nhiên + AI ranking). Auth hoạt động thật (hash mật khẩu, verify token, khóa brute-force); Host CRUD khá đầy đủ.

---

## 0. NHẬT KÝ CẬP NHẬT (phiên 09/07/2026)

### ✅ Luồng đặt phòng — đã chạy End-to-End
- `detail.html`: form đặt phòng đổi từ `GET → trang tĩnh` sang `POST → customer_booking.create_booking`; input thật bằng Bootstrap (chọn phòng, ngày nhận/trả, số khách, ghi chú) + JS cập nhật giá/`action` theo phòng và chặn ngày quá khứ.
- Tạo mới `customer/pages/checkout.html`: xác nhận booking + chọn phương thức (online/cash).
- Tạo mới `customer/pages/mock_payment.html`: cổng thanh toán mô phỏng (success/fail).
- Route `booking.py` giữ nguyên (đã redirect chuẩn `create → checkout → mock_gateway → callback`).
- **Chuỗi hoàn chỉnh:** detail → `HOLDING` (giữ 15') → checkout → gateway mô phỏng → callback → `CONFIRMED`.

### ✅ Killer Feature "Smart Match" — hoàn thành
- Tạo mới `backend/app/services/smart_match.py`: core logic **TF-IDF + cosine similarity** (scikit-learn), đọc DB bằng **Pandas**.
- Công thức xếp hạng: `score = 0.85 × similarity + 0.15 × (rating/5)` (chỉ cộng rating cho phòng có similarity > 0).
- Sinh **"lý do gợi ý"** (khớp tiện ích/địa điểm/sức chứa/thú cưng), có lọc stopword + khử trùng lặp + trích `name` từ service dạng dict.
- Route mới `customer.smart_search` tại `/customer/smart-search?q=...`.
- UI: thêm thanh **Smart Match** vào `search-bar.html`; trang kết quả `home/smart-results.html` (card có **badge % phù hợp**, **số sao**, **chip lý do**).
- `requirements.txt`: thêm `pandas`, `scikit-learn`, `numpy` (đã cài).

---

## 1. BẢNG ĐÁNH GIÁ TIẾN ĐỘ

Chú thích: ✅ Hoàn thành · 🟡 Đang làm / một phần · 🔴 Chưa bắt đầu · 🆕 Cập nhật trong phiên này.

### A. Yêu cầu Chức năng (FR)

#### 2.1 Quản lý tài khoản
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-A-01 | Đăng ký tài khoản | ✅ | Có validate email unique + confirm password. Thiếu policy độ khó mật khẩu. |
| FR-A-02 | Xác thực email | 🟡 | Có token + route `/verify-email/<token>`, nhưng **chỉ giả lập**, chưa gửi email thật (thiếu Flask-Mail/SMTP). |
| FR-A-03 | Đăng nhập + phân quyền | 🟡 | Login/redirect theo role OK. RBAC chưa chặt: nhiều route host thiếu `@login_required`, chưa có `host_required`. |
| FR-A-04 | Quên mật khẩu | 🟡 | Logic token + hạn 1h có, nhưng **thiếu template** `forgot_password.html`, `reset_password.html`. |
| FR-A-05 | Cập nhật thông tin | 🟡 | Host có `profile/edit`. Customer chỉ có trang tĩnh, chưa có route xử lý. Avatar chưa lưu file thật. |
| FR-A-06 | Đăng xuất | ✅ | `/logout` + `logout_user()` chuẩn. |

#### 2.2 Đăng ký cho thuê (Host)
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-H-01 | Đăng ký Host | 🟡 | POST `/customer/become-host` ghi DB, nhưng **thiếu template** `host_registration.html`; upload là mock path. |
| FR-H-02 | Kiểm duyệt hồ sơ | 🟡 | Backend admin có approve/reject, nhưng **seed chưa tạo admin** + **thiếu template** `admin/*.html`. |
| FR-H-03 | Cập nhật Role Host | ✅ (logic) | Admin approve → `role=host`. Bị chặn bởi FR-H-02. |
| FR-H-04 | Quản lý thông tin Host | ✅ | `host/profile` + `profile/edit`. |

#### 2.3 Quản lý nơi cư trú (Property)
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-R-01 | Đăng phòng mới | ✅ | CRUD create. Nhược: hardcode host thay vì `current_user`, chưa bắt buộc Admin duyệt. |
| FR-R-02 | Cập nhật phòng | ✅ | Có edit accommodation + room. |
| FR-R-03 | Quản lý giá (Dynamic pricing) | 🔴 | Chỉ có UI `room/pricing.html`, chưa có route lưu giá theo ngày. |
| FR-R-04 | Quản lý trạng thái | ✅ | Model có status; form set được. |
| FR-R-05 | Quản lý hình ảnh | 🔴 | Chỉ lưu tên file, chưa upload/lưu/xóa ảnh thật. |
| FR-R-06 | Đồng bộ lịch phòng | 🟡 | Có check overlap khi đặt, chưa có bảng block lịch/calendar đúng nghĩa. |

#### 2.4 Đặt phòng (Booking)
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-B-01 | Tìm kiếm phòng | 🟡 🆕 | **Smart Match (AI) đã hoạt động** (`/customer/smart-search`). Bộ lọc cứng truyền thống (ngày/giá/tiện ích) vẫn tĩnh. |
| FR-B-02 | Xem chi tiết | ✅ | `/customer/accommodation/<id>` đọc DB → `detail.html`. |
| FR-B-03 | Giữ phòng tạm thời | ✅ 🆕 | Form đã POST vào `create_booking` → tạo `HOLDING` giữ 15'. Đã nối UI. |
| FR-B-04 | Tạo Booking | ✅ 🆕 | Form `detail.html` nối đúng route; chạy end-to-end. |
| FR-B-05 | Hủy Booking | 🔴 | Có template `trip/cancel-*.html`, chưa có route hủy + release lịch. |
| FR-B-06 | Thông báo Booking | 🔴 | Chưa gửi email/notification. |

#### 2.5 Thanh toán (Payment)
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-P-01 | Thanh toán Online | ✅ (mô phỏng) 🆕 | `checkout.html` + `mock_payment.html` đã tạo; luồng online chạy end-to-end (gateway giả lập). Chưa tích hợp gateway thật. |
| FR-P-02 | Thanh toán Tiền mặt | ✅ (mô phỏng) 🆕 | Checkout cash → confirmed + commission 15%. Đã nối UI. |
| FR-P-03 | Verify giao dịch | 🟡 | Callback giả lập `?status=success`, chưa verify chữ ký thật. |
| FR-P-04 | Cập nhật trạng thái | 🟡 | Có `payment_status`; case "Thất bại" xử lý cơ bản. |
| FR-P-05 | Lịch sử giao dịch | 🟡 | Có `Withdrawal` + trang payment host; `WalletTransaction` chưa có route. |

#### 2.6 Quản lý lưu trú (Stay)
| ID | Tính năng | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| FR-S-01 | Check-in | 🔴 | Chưa có route/logic. |
| FR-S-02 | Check-out | 🔴 | Chưa có route/logic. |
| FR-S-03 | Tranh chấp/Hỗ trợ | 🟡 | Host xem + phản hồi dispute; thiếu luồng customer mở ticket + Admin phân xử. |
| FR-S-04 | Đánh giá (Review) | 🟡 | Có model + seed + hiển thị `average_rating`, nhưng chưa có route tạo/sửa review. |
| FR-S-05 | Trạng thái lưu trú | 🔴 | Chưa có luồng chuyển booking sang completed sau check-out. |

### B. Yêu cầu Phi chức năng (NFR)
| ID | Hạng mục | Trạng thái | Còn thiếu cần bổ sung |
| :--- | :--- | :--- | :--- |
| NFR-01 | Hiệu năng < 3s | ✅ (dev) | Data nhỏ + SQLite nên nhanh; chưa đo tải. |
| NFR-02 | 100 CCU | 🔴 | Dev server + SQLite chưa phục vụ concurrency; cần WSGI + RDBMS. |
| NFR-03 | Bảo mật (hash + HTTPS) | 🟡 | Hash mật khẩu ✅. HTTPS/TLS chưa. |
| NFR-04 | RBAC 3 role | 🟡 | Có role + admin decorator, nhưng host routes hở, còn hardcode `host_id=1`. |
| NFR-05 | Không double booking | 🟡 | Có overlap check khi đặt, chưa có transaction/lock DB → còn race condition. |
| NFR-06 | Chịu lỗi giao dịch | 🟡 | Giữ booking khi lỗi (mock); chưa test kỹ. |
| NFR-07 | Backup định kỳ | 🔴 | Chưa có cơ chế backup. |
| NFR-08 | Khả năng mở rộng | 🟡 | Kiến trúc blueprint tốt, còn hardcode + SQLite. |
| NFR-09 | UI/UX Responsive | ✅ | Bootstrap 5.3 + CSS Figma; đa số trang đã dựng. |
| NFR-10 | Cấu trúc module | ✅ | Application factory + blueprints + models + services tách rõ. |
| NFR-11 | Uptime 99% | 🔴 | Chưa deploy/monitoring. |
| NFR-12 | Usability | 🟡 | Flash message có; thông báo lỗi chưa đồng bộ toàn hệ. |

**Nhận định:** Luồng cốt lõi **search (AI) → book → pay → confirm** giờ đã chạy được end-to-end. Phần còn lại tập trung vào: hủy/booking-lifecycle (check-in/out, cancel, review) và siết RBAC.

---

## 2. KILLER FEATURE — "Smart Match" (ĐÃ HOÀN THÀNH)

**Mô tả:** Tìm kiếm homestay bằng ngôn ngữ tự nhiên + AI ranking, thay cho bộ lọc cứng.

**Kiến trúc:**
- **Đầu vào:** 1 câu tiếng Việt tự do (vd: *"homestay Đà Lạt cho 4 người, có hồ bơi, cho mang thú cưng"*).
- **Xử lý (`backend/app/services/smart_match.py`):**
  1. `load_rooms_dataframe()` — Pandas đọc Room ⋈ Accommodation (chỉ `active`) + `avg_rating` từ bảng reviews.
  2. `build_corpus()` — gộp tên/loại/địa điểm/mô tả/tiện ích/sức chứa thành "văn bản" mỗi phòng.
  3. `smart_match()` — TF-IDF + cosine similarity, trộn điểm rating, sinh "lý do gợi ý".
- **Đầu ra:** Top phòng kèm **% phù hợp**, **số sao**, **chip lý do**, link sang chi tiết → đặt phòng.

**Công thức:** `score = 0.85 × cosine_similarity + 0.15 × (rating / 5)` (rating chỉ cộng khi similarity > 0).

**Thư viện:** `pandas`, `scikit-learn` (`TfidfVectorizer`, `cosine_similarity`), `numpy`.

**Chạy thử nhanh (CLI):**
```bash
py -m backend.app.services.smart_match "phòng cho 2 người có hồ bơi"
```

**Ý tưởng nâng cấp (tùy chọn):** tách từ tiếng Việt bằng `underthesea`; parse tiêu chí giá/ngày bằng regex để lọc cứng thêm; cache TF-IDF matrix.

---

## 3. ĐỀ XUẤT #2 (dự phòng, nếu còn thời gian) — "Insight Dashboard" cho Host
Thay trang `host/report/index.html` (đang 100% mock) bằng phân tích thật từ `Booking`/`Review`: doanh thu theo tháng (Pandas groupby), **dự báo doanh thu** bằng Linear Regression (scikit-learn), cảnh báo "phòng sắp ế". Render biểu đồ qua Chart.js. Dùng chung `pandas` + `scikit-learn`.

---

## 4. VIỆC TIẾP THEO (ưu tiên giảm dần)
1. **Booking lifecycle:** route Hủy booking (release lịch), Check-in/Check-out, cập nhật trạng thái `completed`.
2. **Review:** route tạo/sửa review sau check-out (đóng vòng data cho Smart Match).
3. **Siết RBAC:** thêm decorator `host_required`, bỏ hardcode `host_id=1`, dùng `current_user`.
4. **Admin flow:** seed 1 user admin + tạo template `admin/*.html` để duyệt Host/Accommodation.
5. **Hoàn thiện Auth phụ:** template `forgot_password.html`, `reset_password.html`, `host_registration.html`.
6. **(Tùy chọn)** Insight Dashboard cho Host.
