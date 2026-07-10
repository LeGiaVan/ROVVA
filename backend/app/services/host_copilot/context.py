from datetime import date, timedelta

from backend.app.models import Accommodation, Booking, Room


def get_host_rooms(host_id):
    return (
        Room.query.join(Accommodation)
        .filter(
            Accommodation.host_id == host_id,
            Room.status == Room.STATUS_ACTIVE,
            Accommodation.status == Accommodation.STATUS_ACTIVE,
        )
        .all()
    )


def get_host_bookings(host_id, statuses=None):
    query = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == host_id)
    )
    if statuses:
        query = query.filter(Booking.status.in_(statuses))
    return query.all()


def gather_host_context(host_id):
    today = date.today()
    rooms = get_host_rooms(host_id)
    room_ids = [r.id for r in rooms]
    active_statuses = [
        Booking.STATUS_CONFIRMED,
        Booking.STATUS_COMPLETED,
        "Đang lưu trú",
        "Hoàn thành",
    ]
    bookings = get_host_bookings(host_id, active_statuses)
    cancelled = Booking.query.join(Room).join(Accommodation).filter(
        Accommodation.host_id == host_id,
        Booking.status == Booking.STATUS_CANCELLED,
    ).count()

    next_week_end = today + timedelta(days=7)
    booked_nights_next_week = 0
    for b in bookings:
        if b.status in (Booking.STATUS_CANCELLED, "Đã hủy", "cancelled"):
            continue
        start = max(b.check_in, today)
        end = min(b.check_out, next_week_end)
        if start < end:
            booked_nights_next_week += (end - start).days

    available_nights = len(rooms) * 7
    next_week_occupancy = (
        booked_nights_next_week / available_nights if available_nights else 0
    )

    weekend_nights = 0
    weekend_booked = 0
    for offset in range(7):
        day = today + timedelta(days=offset)
        if day.weekday() >= 5:
            weekend_nights += len(rooms)
            for b in bookings:
                if b.check_in <= day < b.check_out:
                    weekend_booked += 1
    weekend_occ = weekend_booked / weekend_nights if weekend_nights else 0

    weekday_nights = 0
    weekday_booked = 0
    for offset in range(7):
        day = today + timedelta(days=offset)
        if day.weekday() < 5:
            weekday_nights += len(rooms)
            for b in bookings:
                if b.check_in <= day < b.check_out:
                    weekday_booked += 1
    weekday_occ = weekday_booked / weekday_nights if weekday_nights else 0

    nights_list = [b.nights for b in bookings if b.nights > 0]
    avg_nights = sum(nights_list) / len(nights_list) if nights_list else 0

    total_bookings = len(bookings) + cancelled
    cancel_rate = cancelled / total_bookings if total_bookings else 0

    prices = [r.base_price for r in rooms if r.base_price]
    median_price = sorted(prices)[len(prices) // 2] if prices else 0
    underpriced_rooms = [r for r in rooms if r.base_price and r.base_price < median_price * 0.85]

    return {
        "today": today,
        "rooms": rooms,
        "room_ids": room_ids,
        "bookings": bookings,
        "next_week_occupancy": round(next_week_occupancy, 3),
        "weekend_occ": round(weekend_occ, 3),
        "weekday_occ": round(weekday_occ, 3),
        "avg_nights": round(avg_nights, 1),
        "cancel_rate": round(cancel_rate, 3),
        "median_price": median_price,
        "underpriced_rooms": underpriced_rooms,
        "active_room_count": len(rooms),
    }
