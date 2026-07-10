# Hướng dẫn bổ sung ảnh demo cho giao diện ROVVA

Tài liệu này dành cho thành viên team **chỉ cần thả ảnh vào đúng thư mục** — không cần sửa code hay database.

---

## 1. Cơ chế hoạt động

Hệ thống tự suy đường dẫn ảnh theo **ID** của cơ sở lưu trú (CSLT) và phòng:

- Nếu file ảnh **tồn tại** → hiển thị ảnh thật.
- Nếu **chưa có** → hiển thị placeholder SVG (giao diện không bị vỡ).

Logic nằm tại `backend/app/utils/media.py`. Model dùng property `cover_url`, `gallery_urls`, `image_url` — **không lưu đường dẫn ảnh vào DB**.

---

## 2. Quy ước thư mục (bắt buộc)

Tất cả ảnh đặt trong:

```
frontend/static/customer/images/
```

### 2.1. Ảnh CSLT (theo `acc_id`)

```
frontend/static/customer/images/accommodations/<acc_id>/
├── cover.jpg              ← Ảnh đại diện (card, mosaic chính)
├── gallery/
│   ├── 1.jpg
│   ├── 2.jpg
│   ├── 3.jpg
│   ├── 4.jpg
│   └── 5.jpg              ← Mosaic + gallery trang chi tiết
└── rooms/
    ├── <room_id>.jpg      ← Mỗi phòng một file, tên = ID phòng
    └── ...
```

**Ví dụ thực tế:**

```
frontend/static/customer/images/accommodations/1/cover.jpg
frontend/static/customer/images/accommodations/1/gallery/1.jpg
frontend/static/customer/images/accommodations/1/rooms/3.jpg
```

### 2.2. Placeholder (đã có sẵn — không cần sửa)

```
frontend/static/customer/images/placeholders/
├── accommodation.svg
├── room.svg
└── avatar.svg
```

### 2.3. Ảnh tĩnh khác (banner, logo, avatar marketing)

Các ảnh **không** theo ID vẫn dùng đường dẫn cố định trong template:

| Mục đích | Đường dẫn gợi ý |
|----------|------------------|
| Logo header | `customer/images/logos/Logo.jpg` |
| Banner khuyến mãi | `customer/images/banners/P1_Dac_quyen&Khuyen_mai.jpg` |
| Avatar mẫu | `customer/images/avatars/Hinh_avata.jpg` |
| Hero / nền trang chủ | `customer/images/backgrounds/` (nếu template tham chiếu) |

---

## 3. Cách tra ID cơ sở lưu trú & phòng

### Cách 1 — Qua trình duyệt (nhanh nhất)

1. Chạy app: `py run.py`
2. Mở trang chi tiết: `http://127.0.0.1:5000/customer/accommodation/1`
3. Số **`1`** trong URL = `acc_id`
4. Vào trang chi tiết → mở popup từng phòng → xem HTML/modal hoặc dùng cách 2 để biết `room_id`

### Cách 2 — Qua script (chính xác nhất)

Chạy trong thư mục gốc dự án:

```powershell
py -c "
from backend.app import create_app
from backend.app.models import Accommodation, Room
app = create_app()
with app.app_context():
    for acc in Accommodation.query.order_by(Accommodation.id):
        print(f'CSLT #{acc.id}: {acc.name} ({acc.type}) - {acc.city}')
        for r in acc.rooms:
            print(f'  Room #{r.id}: {r.name}')
"
```

Ghi lại cặp `(acc_id, room_id)` tương ứng tên phòng cần chụp ảnh.

### Cách 3 — Sau khi seed (thứ tự mặc định)

Sau `py -m flask --app run seed`, ID gán **theo thứ tự insert** trong `seed.py`:

| acc_id | Tên CSLT |
|--------|----------|
| 1 | Homestay Đà Lạt View |
| 2 | Villa Hội An Garden |
| 3 | Sunside Homestay |
| … | (xem thêm trong `backend/app/seed.py`) |

> **Lưu ý:** Nếu ai đó reset DB hoặc đổi seed, ID có thể thay đổi. Luôn ưu tiên **Cách 2** trước buổi demo.

---

## 4. Yêu cầu kỹ thuật ảnh

| Thuộc tính | Gợi ý |
|------------|--------|
| **Định dạng** | `.jpg` (ưu tiên) hoặc `.jpeg` |
| **Tên file** | Đúng chữ thường như quy ước: `cover.jpg`, `1.jpg`, `<room_id>.jpg` |
| **Kích thước cover** | 1200×800 px trở lên, tỷ lệ ngang 4:3 hoặc 16:9 |
| **Gallery** | 800×600 px trở lên |
| **Ảnh phòng** | 800×600 px, cùng góc chụp để đồng bộ UI |
| **Dung lượng** | &lt; 500 KB/ảnh (nén trước khi commit) |

Công cụ nén gợi ý: [Squoosh](https://squoosh.app), TinyPNG, hoặc export từ Figma ở quality 80%.

---

## 5. Quy trình làm việc cho team

```
1. Chạy seed (nếu DB trống)
      ↓
2. Tra acc_id / room_id (mục 3)
      ↓
3. Tạo thư mục accommodations/<acc_id>/...
      ↓
4. Copy ảnh đúng tên file
      ↓
5. Restart server (Ctrl+C → py run.py)
      ↓
6. Kiểm tra: trang chủ → search → chi tiết CSLT → popup phòng
```

### Checklist trước buổi demo

- [ ] Ít nhất **4 CSLT nổi bật** (acc_id 1–4) có `cover.jpg`
- [ ] Mỗi CSLT demo có **3–5 ảnh gallery**
- [ ] Mỗi phòng hiển thị trên UI có file `rooms/<room_id>.jpg`
- [ ] Logo + banner trang chủ guest không bị 404
- [ ] Hard refresh trình duyệt (`Ctrl+F5`) sau khi thêm ảnh

---

## 6. Phân công gợi ý (5 thành viên)

| Thành viên | Nhiệm vụ ảnh |
|------------|--------------|
| A | CSLT #1–3: cover + gallery |
| B | CSLT #4–6: cover + gallery |
| C | Ảnh phòng (rooms/) cho acc #1–6 |
| D | Banner, logo, avatar marketing |
| E | Kiểm tra UI toàn site + báo thiếu ID |

---

## 7. Lỗi thường gặp

| Triệu chứng | Nguyên nhân | Cách sửa |
|-------------|-------------|----------|
| Vẫn thấy placeholder SVG | Sai tên file hoặc sai thư mục | Kiểm tra đúng `acc_id`, đuôi `.jpg` |
| Ảnh cũ không đổi | Cache trình duyệt | `Ctrl+F5` hoặc mở tab ẩn danh |
| Ảnh phòng sai CSLT | Nhầm `acc_id` | Chạy lại script tra ID (mục 3) |
| 404 static | Đặt nhầm ngoài `frontend/static/` | Di chuyển vào đúng cây thư mục |

---

## 8. Commit lên Git

Chỉ add thư mục ảnh, **không** add file `.db`:

```powershell
git add frontend/static/customer/images/accommodations/
git add frontend/static/customer/images/banners/
git commit -m "Thêm ảnh demo CSLT #1-#4 cho buổi trình bày"
git push
```

Nếu ảnh quá nặng (&gt; 50 MB tổng), cân nhắc nén hoặc dùng Git LFS — hỏi lead trước khi push.

---

## 9. Liên hệ khi cần hỗ trợ

- **Logic ảnh / placeholder:** xem `backend/app/utils/media.py`
- **Dữ liệu demo / ID:** xem `backend/app/seed.py` hoặc hỏi người phụ trách backend
- **UI hiển thị ảnh ở đâu:** trang chủ (`member.html` / `guest.html`), `search-results.html`, `accommodation/detail.html`
