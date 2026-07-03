from flask import Blueprint, render_template, request
from backend.app.models import Booking

booking_bp = Blueprint("booking", __name__, url_prefix="/bookings")

@booking_bp.route("/")
def index():
    status_filter = request.args.get("status", "Tất cả")
    query = Booking.query
    
    if status_filter != "Tất cả":
        query = query.filter(Booking.status == status_filter)
        
    bookings = query.order_by(Booking.created_at.desc()).all()
    
    return render_template(
        "booking/index.html",
        active_nav="bookings",
        active_tab=status_filter,
        bookings=bookings
    )

@booking_bp.route("/<int:id>")
def detail(id):
    booking = Booking.query.get_or_404(id)
    return render_template(
        "booking/detail.html",
        active_nav="bookings",
        booking=booking
    )
