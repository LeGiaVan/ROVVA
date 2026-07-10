PERSONAS = {
    "solo_explorer": {
        "label": "Khách solo khám phá",
        "icon": "bi-backpack",
        "tips": [
            "Gửi gợi ý quán cafe và điểm check-in gần CSLT",
            "Ưu tiên check-in linh hoạt nếu phòng sẵn sàng",
        ],
        "message": (
            "Chào {name}! Rất vui được đón bạn. Nếu cần gợi ý địa điểm "
            "hoặc check-in sớm, cứ nhắn em nhé!"
        ),
    },
    "family": {
        "label": "Gia đình có trẻ",
        "icon": "bi-people-fill",
        "tips": [
            "Chuẩn bị thêm gối/chăn nếu số khách vượt giường",
            "Nhắc cầu thang và khu vực an toàn cho trẻ",
        ],
        "message": (
            "Chào {name}! Em đã chuẩn bị thêm chăn gối cho gia đình. "
            "Nếu cần nôi hoặc ghế ăn dặm, hãy báo em trước nhé!"
        ),
    },
    "long_stay": {
        "label": "Khách ở dài ngày",
        "icon": "bi-laptop",
        "tips": [
            "Đề xuất gói giặt ủi hoặc dọn phòng giữa kỳ",
            "Kiểm tra WiFi và bàn làm việc ổn định",
        ],
        "message": (
            "Chào {name}! Với lưu trú {nights} đêm, em có thể hỗ trợ "
            "dọn phòng giữa kỳ miễn phí. Chúc bạn làm việc vui vẻ!"
        ),
    },
    "celebration": {
        "label": "Kỷ niệm / sinh nhật",
        "icon": "bi-balloon-heart",
        "tips": [
            "Trang trí nhẹ phòng hoặc bánh mini nếu có thể",
            "Giữ không gian yên tĩnh, riêng tư",
        ],
        "message": (
            "Chào {name}! Em thấy chuyến đi đặc biệt của bạn — "
            "em có thể hỗ trợ trang trí nhẹ nếu bạn muốn ạ!"
        ),
    },
    "pet_parent": {
        "label": "Đi cùng thú cưng",
        "icon": "bi-heart",
        "tips": [
            "Chuẩn bị thảm lau chân và bát nước",
            "Nhắc quy định khu vực thú cưng được phép",
        ],
        "message": (
            "Chào {name}! Em đã chuẩn bị sẵn chỗ cho boss nhỏ. "
            "Vui lòng báo em trước giờ đến để em đón tiện nhé!"
        ),
    },
}


def infer_guest_persona(booking):
    note = (booking.guest_note or "").lower()
    guests = booking.guest_count or 1
    nights = booking.nights or 1
    signals = []

    if guests == 1 and nights <= 2:
        signals.append(("solo_explorer", 0.7))
    if guests >= 3:
        signals.append(("family", 0.82))
    if nights >= 4:
        signals.append(("long_stay", 0.78))
    if any(k in note for k in ["sinh nhật", "kỷ niệm", "anniversary", "cầu hôn"]):
        signals.append(("celebration", 0.92))
    if any(k in note for k in ["trẻ", "bé", "con", "em bé", "baby"]):
        signals.append(("family", 0.9))
    if any(k in note for k in ["pet", "chó", "mèo", "thú cưng", "cún"]):
        signals.append(("pet_parent", 0.95))
    if any(k in note for k in ["chăn", "gối", "giường phụ"]):
        signals.append(("family", 0.75))

    acc = booking.room.accommodation if booking.room else None
    if acc and acc.allows_pets and any(
        k in note for k in ["pet", "chó", "mèo", "thú cưng"]
    ):
        signals.append(("pet_parent", 0.98))

    if not signals:
        if guests >= 2:
            signals.append(("family", 0.55))
        else:
            signals.append(("solo_explorer", 0.5))

    signals.sort(key=lambda x: x[1], reverse=True)
    persona_key, confidence = signals[0]
    meta = PERSONAS[persona_key]
    message = meta["message"].format(
        name=booking.guest_name.split()[0] if booking.guest_name else "bạn",
        nights=nights,
    )

    return {
        "key": persona_key,
        "label": meta["label"],
        "icon": meta["icon"],
        "confidence": int(confidence * 100),
        "tips": meta["tips"],
        "message": message,
        "signals": [
            {"guests": guests, "nights": nights, "has_note": bool(note)}
        ],
    }
