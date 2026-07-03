from flask import Blueprint, render_template

from backend.app.models import Accommodation
from backend.app.seed import get_dashboard_stats

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    stats = get_dashboard_stats()
    return render_template(
        "index.html",
        active_nav="dashboard",
        stats=stats,
        accommodations=Accommodation.query.limit(5).all(),
    )
