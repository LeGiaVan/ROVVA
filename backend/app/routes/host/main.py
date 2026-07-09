from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user

from backend.app.models import Accommodation, Booking, User
from backend.app.seed import get_dashboard_stats

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
@login_required
def index():
    stats = get_dashboard_stats()
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(4).all()
    host = current_user
    
    # Adding mock growth data for the UI
    stats["revenue_growth"] = "+12.5%"
    stats["new_bookings"] = 8
    
    from backend.app.models.room import Room
    from backend.app.models.accommodation import Accommodation
    
    # Get all bookings for the current host
    host_bookings = Booking.query.join(Room).join(Accommodation).filter(
        Accommodation.host_id == current_user.id
    ).all()
    
    total_revenue = 0
    disbursed_pool = 0
    disputed_amount = 0
    
    for b in host_bookings:
        if b.status in [Booking.STATUS_CONFIRMED, "Hoàn thành", "Đang lưu trú"]:
            total_revenue += b.total_amount
            if b.payment_status == "disbursed":
                disbursed_pool += b.total_amount
            elif b.payment_status == "in_dispute":
                disputed_amount += b.total_amount

    stats["pending_payout"] = total_revenue
    stats["disbursed_amount"] = max(0, disbursed_pool - disputed_amount)
    stats["disputed_amount"] = disputed_amount
    stats["total_revenue"] = total_revenue
    
    return render_template(
        "host/index.html",
        active_nav="dashboard",
        stats=stats,
        recent_bookings=recent_bookings,
        host=host
    )

@main_bp.route("/profile")
@login_required
def profile():
    return render_template(
        "host/profile.html",
        active_nav="profile",
        host=current_user
    )

@main_bp.route("/profile/edit", methods=["POST"])
@login_required
def edit_profile():
    from backend.app.extensions import db
    import os
    from werkzeug.utils import secure_filename
    
    user = current_user
    user.full_name = request.form.get("full_name", user.full_name)
    user.email = request.form.get("email", user.email)
    user.phone = request.form.get("phone", user.phone)
    user.id_card = request.form.get("id_card", user.id_card)
    user.introduction = request.form.get("introduction", user.introduction)
    
    # Minimal avatar upload handling
    if "avatar" in request.files:
        file = request.files["avatar"]
        if file.filename != "":
            filename = secure_filename(file.filename)
            # normally save to a proper uploads folder
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # for now just pretend it's saved in images/
            user.avatar = f"images/{filename}"
            
    db.session.commit()
    return redirect(url_for("main.profile"))

@main_bp.route("/profile/change-password", methods=["POST"])
@login_required
def change_password():
    from backend.app.extensions import db
    from flask import flash
    
    user = current_user
    current_password = request.form.get("current_password")
    new_password = request.form.get("new_password")
    confirm_password = request.form.get("confirm_password")
    
    if not user.check_password(current_password):
        flash("Mật khẩu hiện tại không đúng.", "error")
        return redirect(url_for("main.profile"))
        
    if new_password != confirm_password:
        flash("Mật khẩu mới không khớp.", "error")
        return redirect(url_for("main.profile"))
        
    user.set_password(new_password)
    db.session.commit()
    flash("Đổi mật khẩu thành công.", "success")
    return redirect(url_for("main.profile"))
