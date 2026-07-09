# TÀI LIỆU ĐẶC TẢ YÊU CẦU HỆ THỐNG (SRS) - DỰ ÁN HOMESTAY

Tài liệu này cung cấp toàn bộ bối cảnh nghiệp vụ, yêu cầu chức năng (FR), yêu cầu phi chức năng (NFR) và các luồng quy trình (BPMN) để phát triển hệ thống Homestay đa người dùng (Customer, Host, Admin).

---

## 1. YÊU CẦU PHI CHỨC NĂNG (NON-FUNCTIONAL REQUIREMENTS - NFR)

Ràng buộc hệ thống, tiêu chuẩn kỹ thuật và các yếu tố chất lượng bắt buộc.

| Mã số | Hạng mục | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| **NFR-01** | Hiệu năng | Thời gian phản hồi các chức năng chính (tìm kiếm, đăng nhập, đặt phòng) < 3s (tải bình thường). | Cao |
| **NFR-02** | Hiệu năng | Hỗ trợ tối thiểu 100 CCU (người dùng truy cập đồng thời) không giảm hiệu suất. | Cao |
| **NFR-03** | Bảo mật | Mật khẩu phải mã hóa (Hash); Truyền tải dữ liệu qua HTTPS/TLS. | Cao |
| **NFR-04** | Phân quyền | Áp dụng Role-based Access Control (RBAC): Khách hàng, Host, Admin. | Cao |
| **NFR-05** | Toàn vẹn dữ liệu | **Tuyệt đối không** xảy ra double booking (đặt trùng phòng) trong cùng thời gian. | Cao |
| **NFR-06** | Chịu lỗi | Xử lý lỗi giao dịch/thanh toán không làm mất dữ liệu booking hiện tại. | Cao |
| **NFR-07** | Backup | Dữ liệu phải được sao lưu tự động định kỳ. | Cao |
| **NFR-08** | Mở rộng | Kiến trúc hỗ trợ scale số lượng người dùng và phòng trong tương lai. | Trung bình |
| **NFR-09** | UI/UX | Giao diện trực quan, Responsive (tương thích Web/Mobile). | Cao |
| **NFR-10** | Bảo trì | Mã nguồn cấu trúc module rõ ràng (Modular architecture). | Trung bình |
| **NFR-11** | Uptime | Đảm bảo thời gian hoạt động (Uptime) tối thiểu 99%. | Cao |
| **NFR-12** | Usability | Tối ưu số bước thao tác; Thông báo lỗi phải rõ ràng cho end-user. | Trung bình |

---

## 2. YÊU CẦU CHỨC NĂNG (FUNCTIONAL REQUIREMENTS - FR)

### 2.1 Quản lý tài khoản (Account Management)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-A-01 | Đăng ký tài khoản | Đăng ký bằng email, mật khẩu, thông tin cơ bản. Validate dữ liệu đầu vào. | Cao |
| FR-A-02 | Xác thực email | Gửi email chứa link/OTP để kích hoạt tài khoản. | Cao |
| FR-A-03 | Đăng nhập hệ thống | Đăng nhập bằng Email/Password; Phân quyền theo Role. | Cao |
| FR-A-04 | Quên mật khẩu | Yêu cầu reset password qua email đã đăng ký. | Cao |
| FR-A-05 | Cập nhật thông tin | Đổi họ tên, SĐT, avatar. | Trung bình |
| FR-A-06 | Đăng xuất | Kết thúc session/token, quay về trang chủ. | Trung bình |

### 2.2 Đăng ký cho thuê (Host Registration)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-H-01 | Đăng ký Host | Gửi yêu cầu + cung cấp thông tin/giấy tờ kinh doanh để thành Host. | Cao |
| FR-H-02 | Kiểm duyệt thông tin | Hệ thống (Admin) kiểm tra tính hợp lệ của hồ sơ. | Cao |
| FR-H-03 | Cập nhật Role Host | Chuyển Role -> Host sau khi duyệt thành công. | Cao |
| FR-H-04 | Quản lý thông tin Host | Host cập nhật profile kinh doanh/cho thuê. | Trung bình |

### 2.3 Quản lý nơi cư trú (Property Management)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-R-01 | Đăng phòng mới | Host tạo phòng: Mô tả, địa chỉ, giá, tiện ích (Cần Admin duyệt). | Cao |
| FR-R-02 | Cập nhật phòng | Chỉnh sửa thông tin phòng đã đăng. | Cao |
| FR-R-03 | Quản lý giá thuê | Thiết lập/cập nhật giá theo thời điểm (Dynamic pricing). | Trung bình |
| FR-R-04 | Quản lý trạng thái | Đổi trạng thái: Trống, Đã đặt, Tạm ngừng hoạt động. | Cao |
| FR-R-05 | Quản lý hình ảnh | Upload, xóa, sửa ảnh minh họa phòng. | Trung bình |
| FR-R-06 | Đồng bộ lịch phòng | Tự động block lịch khi có booking thành công. | Cao |

### 2.4 Đặt phòng (Booking Workflow)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-B-01 | Tìm kiếm phòng | Bộ lọc: Địa điểm, thời gian, số khách, giá, tiện ích. | Cao |
| FR-B-02 | Xem chi tiết | Hiển thị full thông tin phòng trước khi đặt. | Cao |
| FR-B-03 | Giữ phòng tạm thời | Lock phòng (Giữ chỗ) trong lúc chờ thanh toán. | Cao |
| FR-B-04 | Tạo Booking | Lưu record booking khi hoàn tất quy trình. | Cao |
| FR-B-05 | Hủy Booking | Hủy theo chính sách của Host/Hệ thống. | Trung bình |
| FR-B-06 | Thông báo Booking | Gắn trigger gửi Email/Noti cho Host và Khách. | Trung bình |

### 2.5 Thanh toán (Payment)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-P-01 | Thanh toán Online | Chuyển khoản trực tuyến qua Payment Gateway. | Cao |
| FR-P-02 | Thanh toán Tiền mặt | Trả tiền mặt khi check-in (Tùy chính sách Host). | Trung bình |
| FR-P-03 | Verify Giao dịch | Xác minh callback từ Gateway trước khi chốt Booking. | Cao |
| FR-P-04 | Cập nhật trạng thái | Đổi status: "Đã thanh toán" / "Thất bại". | Cao |
| FR-P-05 | Lịch sử giao dịch | Lưu log để đối soát, tra cứu. | Trung bình |

### 2.6 Quản lý lưu trú (Stay/Check-in Management)
| Mã số | Yêu cầu chức năng | Mô tả chi tiết | Ưu tiên |
| :--- | :--- | :--- | :--- |
| FR-S-01 | Check-in | Khách thao tác nhận phòng cho booking hợp lệ. | Cao |
| FR-S-02 | Check-out | Khách thao tác trả phòng. | Cao |
| FR-S-03 | Tranh chấp/Hỗ trợ | Mở ticket report/hỗ trợ trong thời gian ở. | Trung bình |
| FR-S-04 | Đánh giá (Review) | Rate & Review sau khi check-out thành công. | Trung bình |
| FR-S-05 | Trạng thái lưu trú | Cập nhật status check-in/check-out của record booking. | Cao |

---

## 3. QUY TRÌNH NGHIỆP VỤ (BUSINESS PROCESSES & RULES)

### 3.1 Quy trình Đăng ký & Đăng nhập (Auth Flow)
* **Mô tả:** Quản lý luồng truy cập và xác thực. Khách hàng đăng ký -> Kích hoạt Email -> Đăng nhập. Người dùng có thể nâng cấp lên Host (chờ Admin duyệt).
* **Quy tắc nghiệp vụ (Business Rules):**
  - `Email` là Unique Key (1 email = 1 account).
  - Phải Verify Email mới được phép Login.
  - Cấp quyền Host = `Pending` -> `Admin Approved` -> `Active`.
  - Mật khẩu cần policy độ khó. Link reset password có thời hạn.
  - Log lại lịch sử thay đổi quyền (Audit log).
  - Tạm khóa tài khoản nếu login sai nhiều lần (Brute-force protection).
* **Ngoại lệ (Exceptions):**
  - Trùng Email -> Báo lỗi.
  - Link reset hết hạn -> Request link mới.

### 3.2 Quy trình Đăng ký cho thuê (Host Onboarding)
* **Mô tả:** User submit form thông tin/giấy tờ -> Chờ duyệt -> Admin check -> Approve/Reject.
* **Quy tắc nghiệp vụ:**
  - Yêu cầu Auth (Must be logged in).
  - Yêu cầu Submit 1 lần duy nhất cho 1 Account.
  - Chỉ Admin mới có quyền đổi trạng thái Role -> Host.
  - Giấy tờ upload phải validate định dạng/dung lượng (e.g., PDF/JPG, < 5MB).
  - Nếu bị Reject, cho phép update và re-submit.
* **Ngoại lệ:**
  - Đã là Host -> Chặn truy cập form.
  - Upload file sai -> Báo lỗi UI ngay lập tức.

### 3.3 Quy trình Đặt phòng (Booking Flow)
* **Mô tả:** Khách tìm phòng trống -> Xem chi tiết -> Nhập thông tin đặt -> Hệ thống khóa phòng (Hold) -> Thanh toán -> Sinh Booking Record.
* **Quy tắc nghiệp vụ:**
  - Chỉ hiển thị phòng trạng thái `Active` và không bị block lịch trong ngày khách chọn.
  - **Critical:** Phải check lại Availability tại giây phút nhấn "Đặt phòng" (tránh race condition).
  - Trạng thái `Hold`: Tự động giải phóng (Release) nếu quá hạn thanh toán (VD: 15 phút).
  - Phòng đang `Hold` hoặc `Booked` -> Ẩn khỏi kết quả tìm kiếm ngày đó.
  - Hủy phòng (Cancel) -> Release lịch -> Hiển thị lại trên trang tìm kiếm.
  - 1 User không được đặt trùng thời gian cho cùng 1 phòng (Spam protection).
* **Ngoại lệ:**
  - Có người khác nhanh tay hơn -> Báo "Phòng không còn khả dụng".
  - Hết time giữ phòng -> Hủy session đặt phòng.

### 3.4 Quy trình Thanh toán (Payment Flow)
* **Mô tả:** Booking ở trạng thái `Pending Payment` -> Chọn hình thức -> Gọi Gateway/Tiền mặt -> Xử lý Callback -> Đổi trạng thái Booking & Phòng -> Thông báo.
* **Quy tắc nghiệp vụ:**
  - Checkout thành công -> Trạng thái Booking = `Confirmed`, Trạng thái lịch phòng = `Booked`.
  - Tiền mặt -> Trạng thái Payment update thủ công khi Host xác nhận.
  - Hệ thống tính phí hoa hồng (Commission) tự động để đối soát với Host sau này.
  - Lưu mã Transaction ID của bên thứ 3.
* **Ngoại lệ:**
  - User tắt trình duyệt khi thanh toán -> Booking hết hạn -> Tự hủy.
  - Lỗi Gateway -> Giữ booking `Pending Payment` để user thử lại.
  - Tiền đã trừ nhưng Callback lỗi -> Cần cơ chế Admin đối soát tay.

### 3.5 Quy trình Quản lý Nơi cư trú (Property/Stay Management)
* **Mô tả:** Host tạo phòng mới -> Chờ Admin duyệt -> Hiển thị public -> Host chỉnh sửa, quản lý giá, quản lý lịch (Block/Unblock).
* **Quy tắc nghiệp vụ:**
  - Chỉ Role `Host` được truy cập.
  - Phòng tạo mới/Sửa thông tin nhạy cảm -> Cần Admin duyệt lại (`Pending Approval`).
  - Lịch sử update phải được lưu lại.
  - Cho phép cấu hình giá linh hoạt (Ngày thường vs Cuối tuần).
  - Khi Host chủ động "Tạm ngừng" phòng -> Ẩn public, nhưng KHÔNG ảnh hưởng các booking đã Confirmed.
* **Ngoại lệ:**
  - Đang sửa phòng thì có khách đặt -> Cảnh báo đồng bộ.