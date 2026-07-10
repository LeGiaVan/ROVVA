"""Trợ giúp phân giải đường dẫn ảnh với cơ chế fallback placeholder.

Quy ước thư mục (đặt trong frontend/static/):
    customer/images/accommodations/<acc_id>/cover.jpg
    customer/images/accommodations/<acc_id>/gallery/1..5.jpg
    customer/images/accommodations/<acc_id>/rooms/<room_id>.jpg

Nếu file chưa được "thả" vào thư mục, trả ảnh placeholder tương ứng để
giao diện không bị vỡ. Nhờ vậy có thể bổ sung ảnh demo dần mà không cần sửa code.
"""

import os

from flask import current_app, url_for

PLACEHOLDERS = {
    "accommodation": "customer/images/placeholders/accommodation.svg",
    "room": "customer/images/placeholders/room.svg",
    "avatar": "customer/images/placeholders/avatar.svg",
}


def _static_exists(rel_path):
    static_folder = current_app.static_folder
    if not static_folder or not rel_path:
        return False
    full_path = os.path.join(static_folder, *rel_path.split("/"))
    return os.path.isfile(full_path)


def resolve_media(rel_path, kind="accommodation"):
    """Trả URL tĩnh nếu file tồn tại, ngược lại trả placeholder theo `kind`."""
    if rel_path and _static_exists(rel_path):
        return url_for("static", filename=rel_path)
    placeholder = PLACEHOLDERS.get(kind, PLACEHOLDERS["accommodation"])
    return url_for("static", filename=placeholder)


def accommodation_cover(acc_id):
    return resolve_media(
        f"customer/images/accommodations/{acc_id}/cover.jpg", "accommodation"
    )


def accommodation_gallery(acc_id, count=5):
    return [
        resolve_media(
            f"customer/images/accommodations/{acc_id}/gallery/{i}.jpg", "accommodation"
        )
        for i in range(1, count + 1)
    ]


def room_image(acc_id, room_id):
    return resolve_media(
        f"customer/images/accommodations/{acc_id}/rooms/{room_id}.jpg", "room"
    )
