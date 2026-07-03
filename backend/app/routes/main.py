from flask import Blueprint, render_template

from backend.app.models import Accommodation, Booking, User
from backend.app.seed import get_dashboard_stats

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    stats = get_dashboard_stats()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(4).all()
    host = User.query.first() # Using first user as host for demo
    
    # Adding mock growth data for the UI
    stats["revenue_growth"] = "+12.5%"
    stats["new_bookings"] = 8
    
    return render_template(
        "index.html",
        active_nav="dashboard",
        stats=stats,
        recent_bookings=recent_bookings,
        host=host
    )
