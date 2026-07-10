from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from backend.app.models import Accommodation, Booking, Room
from backend.app.services.host_copilot import infer_guest_persona

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")


def _host_booking_or_404(booking_id):
    return (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(
            Booking.id == booking_id,
            Accommodation.host_id == current_user.id,
        )
        .first_or_404()
    )


@booking_bp.route("/")
@login_required
def index():
    status_filter = request.args.get("status", "Tất cả")
    query = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(Accommodation.host_id == current_user.id)
    )

    if status_filter != "Tất cả":
        query = query.filter(Booking.status == status_filter)

    bookings = query.order_by(Booking.created_at.desc()).all()

    return render_template(
        "host/booking/index.html",
        active_nav="bookings",
        active_tab=status_filter,
        bookings=bookings,
    )


@booking_bp.route("/<int:id>")
@login_required
def detail(id):
    booking = _host_booking_or_404(id)
    persona = infer_guest_persona(booking)
    return render_template(
        "host/booking/detail.html",
        active_nav="bookings",
        booking=booking,
        persona=persona,
    )
