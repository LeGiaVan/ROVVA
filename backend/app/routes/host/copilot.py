from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required

from backend.app.services.host_copilot import (
    build_recommendations,
    gather_host_context,
    infer_guest_persona,
    scan_maintenance_issues,
)

copilot_bp = Blueprint("copilot", __name__, url_prefix="/copilot")


def _resolved_keys():
    return set(session.get("copilot_resolved", []))


@copilot_bp.route("/")
@login_required
def index():
    host_id = current_user.id
    tab = request.args.get("tab", "advisor")
    resolved = _resolved_keys()

    recommendations, ctx = build_recommendations(host_id, resolved)
    alerts = scan_maintenance_issues(host_id, resolved)

    return render_template(
        "host/copilot/index.html",
        active_nav="copilot",
        active_tab=tab,
        recommendations=recommendations,
        alerts=alerts,
        ctx=ctx,
    )


@copilot_bp.route("/maintenance/resolve", methods=["POST"])
@login_required
def resolve_maintenance():
    key = request.form.get("issue_key", "").strip()
    if key:
        resolved = list(_resolved_keys())
        if key not in resolved:
            resolved.append(key)
        session["copilot_resolved"] = resolved
        flash("Đã đánh dấu xử lý xong.", "success")
    return redirect(url_for("copilot.index", tab="radar"))


@copilot_bp.route("/persona/<int:booking_id>")
@login_required
def booking_persona(booking_id):
    from backend.app.models import Accommodation, Booking, Room

    booking = (
        Booking.query.join(Room)
        .join(Accommodation)
        .filter(
            Booking.id == booking_id,
            Accommodation.host_id == current_user.id,
        )
        .first_or_404()
    )
    persona = infer_guest_persona(booking)
    return render_template(
        "host/copilot/_persona_card.html",
        booking=booking,
        persona=persona,
    )
