"""
Điền ảnh demo cho toàn bộ Accommodation/Room.

1. Sửa tên file phòng theo room_id thật (DB).
2. Copy ảnh từ CSLT đã có sang CSLT thiếu (theo loại hình).
3. Tải thêm ảnh miễn phí (Unsplash) cho hotel/resort/căn hộ để đa dạng demo.
"""

from __future__ import annotations

import shutil
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
IMG_ROOT = ROOT / "frontend" / "static" / "customer" / "images" / "accommodations"

# Donor theo loại hình (acc_id đã có ảnh)
TYPE_DONOR = {
    "Homestay": 1,
    "Villa": 2,
    "Khách sạn": 3,
    "Resort": 6,
    "Cottage": 6,
    "Căn hộ": 2,
}

# Ảnh Unsplash (license miễn phí, dùng cho demo) — hotel / resort / apartment / mountain
EXTRA_COVERS = {
    4: "https://images.unsplash.com/photo-1566073771259-6a8506099945?w=1400&h=900&fit=crop",   # hotel
    5: "https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=1400&h=900&fit=crop",   # resort pool
    9: "https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=1400&h=900&fit=crop",   # boutique hotel
    10: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=1400&h=900&fit=crop",  # apartment
    11: "https://images.unsplash.com/photo-1493809842364-78817add7ffb?w=1400&h=900&fit=crop",  # urban loft
    12: "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1400&h=900&fit=crop",  # mountain
}


def _ensure_dirs(acc_id: int):
    base = IMG_ROOT / str(acc_id)
    (base / "gallery").mkdir(parents=True, exist_ok=True)
    (base / "rooms").mkdir(parents=True, exist_ok=True)
    return base


def _copy_file(src: Path, dst: Path):
    if not src.is_file():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.exists() and dst.stat().st_size == src.stat().st_size:
        return True
    shutil.copy2(src, dst)
    return True


def _download(url: str, dst: Path) -> bool:
    try:
        dst.parent.mkdir(parents=True, exist_ok=True)
        req = urllib.request.Request(url, headers={"User-Agent": "ROVVA-demo-seed/1.0"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            dst.write_bytes(resp.read())
        return dst.is_file() and dst.stat().st_size > 10_000
    except Exception as exc:  # noqa: BLE001
        print(f"  [skip download] {dst.name}: {exc}")
        return False


def fix_room_ids_by_index(acc_id: int, room_ids: list[int]):
    """Đổi rooms/1.jpg … rooms/N.jpg → rooms/<room_id>.jpg nếu file theo index."""
    rooms_dir = IMG_ROOT / str(acc_id) / "rooms"
    if not rooms_dir.is_dir():
        return
    indexed = sorted(
        (p for p in rooms_dir.glob("*.jpg") if p.stem.isdigit() and int(p.stem) <= len(room_ids)),
        key=lambda p: int(p.stem),
    )
    if not indexed:
        return
    # Hai bước để tránh ghi đè khi index trùng room_id (vd. 5.jpg -> room#9 nhưng 5.jpg đã là output cũ)
    temp_pairs: list[tuple[Path, int]] = []
    for i, room_id in enumerate(room_ids[: len(indexed)]):
        src = rooms_dir / f"{i + 1}.jpg"
        if not src.is_file():
            continue
        tmp = rooms_dir / f"__tmp_{room_id}.jpg"
        shutil.copy2(src, tmp)
        temp_pairs.append((tmp, room_id))
    for tmp, room_id in temp_pairs:
        dst = rooms_dir / f"{room_id}.jpg"
        shutil.copy2(tmp, dst)
        tmp.unlink(missing_ok=True)
        print(f"  acc#{acc_id} room index -> room#{room_id}.jpg")
    for i in range(1, len(room_ids) + 1):
        legacy = rooms_dir / f"{i}.jpg"
        if legacy.is_file() and int(legacy.stem) != room_ids[i - 1]:
            legacy.unlink(missing_ok=True)


def fill_from_donor(acc_id: int, acc_type: str, room_ids: list[int], donor_id: int | None = None):
    donor_id = donor_id or TYPE_DONOR.get(acc_type, 1)
    donor = IMG_ROOT / str(donor_id)
    target = _ensure_dirs(acc_id)

    # cover
    if not (target / "cover.jpg").is_file():
        _copy_file(donor / "cover.jpg", target / "cover.jpg")
        print(f"  acc#{acc_id} cover <- acc#{donor_id}")

    # gallery 1..5
    for i in range(1, 6):
        dst = target / "gallery" / f"{i}.jpg"
        if not dst.is_file():
            _copy_file(donor / "gallery" / f"{i}.jpg", dst)

    # rooms
    donor_rooms = sorted((donor / "rooms").glob("*.jpg")) if (donor / "rooms").is_dir() else []
    for idx, room_id in enumerate(room_ids):
        dst = target / "rooms" / f"{room_id}.jpg"
        if dst.is_file():
            continue
        if donor_rooms:
            src = donor_rooms[idx % len(donor_rooms)]
            _copy_file(src, dst)
            print(f"  acc#{acc_id} room#{room_id} <- {src.name} (donor#{donor_id})")
        else:
            gal = donor / "gallery" / f"{(idx % 5) + 1}.jpg"
            _copy_file(gal, dst)


def main():
    from backend.app import create_app
    from backend.app.models import Accommodation

    app = create_app()
    with app.app_context():
        accs = Accommodation.query.order_by(Accommodation.id).all()

        print("=== Bước 1: Sửa room_id theo index ===")
        for acc in accs:
            room_ids = [r.id for r in acc.rooms.order_by("id").all()]
            if room_ids:
                fix_room_ids_by_index(acc.id, room_ids)

        print("\n=== Bước 2: Fill từ donor + tải ảnh ===")
        for acc in accs:
            room_ids = [r.id for r in acc.rooms.order_by("id").all()]
            base = _ensure_dirs(acc.id)
            has_cover = (base / "cover.jpg").is_file()

            if acc.id in EXTRA_COVERS and not has_cover:
                print(f"acc#{acc.id} ({acc.name}): download cover")
                _download(EXTRA_COVERS[acc.id], base / "cover.jpg")

            if not (base / "cover.jpg").is_file() or len(list((base / "gallery").glob("*.jpg"))) < 5:
                print(f"acc#{acc.id} ({acc.type} - {acc.name}): fill from donor")
                fill_from_donor(acc.id, acc.type, room_ids)
            elif room_ids:
                missing = [
                    rid for rid in room_ids
                    if not (base / "rooms" / f"{rid}.jpg").is_file()
                ]
                if missing:
                    print(f"acc#{acc.id} ({acc.name}): fill {len(missing)} missing rooms")
                    fill_from_donor(acc.id, acc.type, room_ids)

            # Đảm bảo gallery đủ 5 ảnh (dùng cover nếu thiếu)
            cover = base / "cover.jpg"
            for i in range(1, 6):
                g = base / "gallery" / f"{i}.jpg"
                if not g.is_file() and cover.is_file():
                    _copy_file(cover, g)

            # CSLT không có phòng: vẫn cần cover + gallery
            if not room_ids and not (base / "cover.jpg").is_file():
                fill_from_donor(acc.id, acc.type, [])

        print("\n=== Bước 3: Báo cáo ===")
        for acc in accs:
            base = IMG_ROOT / str(acc.id)
            cover = (base / "cover.jpg").is_file()
            gal = len(list((base / "gallery").glob("*.jpg"))) if (base / "gallery").is_dir() else 0
            room_ids = [r.id for r in acc.rooms.order_by("id").all()]
            rooms_ok = sum(1 for rid in room_ids if (base / "rooms" / f"{rid}.jpg").is_file())
            status = "OK" if cover and gal >= 3 and (not room_ids or rooms_ok == len(room_ids)) else "THIẾU"
            print(f"  acc#{acc.id:2} [{status:4}] cover={cover} gallery={gal} rooms={rooms_ok}/{len(room_ids)} | {acc.name}")


if __name__ == "__main__":
    main()
