from functools import wraps

from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from sqlalchemy import func

from backend.app.extensions import db
from backend.app.models import (
    Accommodation,
    Booking,
    Dispute,
    Promotion,
    Room,
    User,
)
from backend.app.routes.admin import admin_bp


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Bạn không có quyền truy cập trang này.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


def _dashboard_stats():
    bookings = Booking.query.all()
    revenue = sum(
        b.total_amount or 0
        for b in bookings
        if b.status in (Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED)
    )
    completed = sum(1 for b in bookings if b.status == Booking.STATUS_COMPLETED)
    total_bookings = len(bookings)
    completion_rate = round(completed / total_bookings * 100, 1) if total_bookings else 0

    return {
        "revenue": revenue,
        "booking_count": total_bookings,
        "customer_count": User.query.filter_by(role="guest").count(),
        "host_count": User.query.filter_by(role="host").count(),
        "dispute_count": Dispute.query.filter(
            Dispute.status != Dispute.STATUS_RESOLVED
        ).count(),
        "completion_rate": completion_rate,
        "pending_hosts": User.query.filter_by(host_status="pending").count(),
        "pending_accs": Accommodation.query.filter_by(
            status=Accommodation.STATUS_PENDING
        ).count(),
        "recent_bookings": Booking.query.order_by(Booking.created_at.desc()).limit(5).all(),
    }


@admin_bp.route("/")
@admin_required
def index():
    stats = _dashboard_stats()
    top_accs = (
        db.session.query(
            Accommodation.name,
            func.sum(Booking.total_amount).label("total"),
        )
        .join(Room, Room.accommodation_id == Accommodation.id)
        .join(Booking, Booking.room_id == Room.id)
        .filter(Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_COMPLETED]))
        .group_by(Accommodation.id)
        .order_by(func.sum(Booking.total_amount).desc())
        .limit(5)
        .all()
    )
    return render_template("admin/index.html", stats=stats, top_accs=top_accs)


@admin_bp.route("/customers")
@admin_required
def customers():
    users = User.query.filter_by(role="guest").order_by(User.created_at.desc()).all()
    return render_template("admin/customers.html", users=users)


@admin_bp.route("/hosts")
@admin_required
def hosts():
    pending_hosts = User.query.filter_by(host_status="pending").all()
    approved_hosts = User.query.filter_by(role="host").all()
    return render_template(
        "admin/hosts.html", pending=pending_hosts, approved=approved_hosts
    )


@admin_bp.route("/hosts/<int:user_id>/approve", methods=["POST"])
@admin_required
def approve_host(user_id):
    user = User.query.get_or_404(user_id)
    if user.host_status == "pending":
        user.host_status = "approved"
        user.role = "host"
        db.session.commit()
        flash(f"Đã duyệt tài khoản Host: {user.email}", "success")
    return redirect(url_for("admin.hosts"))


@admin_bp.route("/hosts/<int:user_id>/reject", methods=["POST"])
@admin_required
def reject_host(user_id):
    user = User.query.get_or_404(user_id)
    if user.host_status == "pending":
        user.host_status = "rejected"
        db.session.commit()
        flash(f"Đã từ chối tài khoản Host: {user.email}", "success")
    return redirect(url_for("admin.hosts"))


@admin_bp.route("/accommodations")
@admin_required
def accommodations():
    pending_accs = Accommodation.query.filter_by(
        status=Accommodation.STATUS_PENDING
    ).all()
    active_accs = Accommodation.query.filter_by(
        status=Accommodation.STATUS_ACTIVE
    ).order_by(Accommodation.name).all()
    return render_template(
        "admin/accommodations.html", pending=pending_accs, active=active_accs
    )


@admin_bp.route("/accommodations/<int:acc_id>/approve", methods=["POST"])
@admin_required
def approve_accommodation(acc_id):
    acc = Accommodation.query.get_or_404(acc_id)
    if acc.status == Accommodation.STATUS_PENDING:
        acc.status = Accommodation.STATUS_ACTIVE
        for room in acc.rooms:
            if room.status == Room.STATUS_PENDING:
                room.status = Room.STATUS_ACTIVE
        db.session.commit()
        flash(f"Đã duyệt chỗ nghỉ: {acc.name}", "success")
    return redirect(url_for("admin.accommodations"))


@admin_bp.route("/accommodations/<int:acc_id>/reject", methods=["POST"])
@admin_required
def reject_accommodation(acc_id):
    acc = Accommodation.query.get_or_404(acc_id)
    if acc.status == Accommodation.STATUS_PENDING:
        acc.status = Accommodation.STATUS_REJECTED
        db.session.commit()
        flash(f"Đã từ chối chỗ nghỉ: {acc.name}", "success")
    return redirect(url_for("admin.accommodations"))


@admin_bp.route("/rooms")
@admin_required
def rooms():
    rooms = Room.query.order_by(Room.id.desc()).all()
    return render_template("admin/rooms.html", rooms=rooms)


@admin_bp.route("/bookings")
@admin_required
def bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return render_template("admin/bookings.html", bookings=bookings)


@admin_bp.route("/disputes")
@admin_required
def disputes():
    items = Dispute.query.order_by(Dispute.created_at.desc()).all()
    return render_template("admin/disputes.html", disputes=items)


@admin_bp.route("/disputes/<int:dispute_id>/resolve", methods=["POST"])
@admin_required
def resolve_dispute(dispute_id):
    dispute = Dispute.query.get_or_404(dispute_id)
    resolution = request.form.get("admin_resolution", "").strip()
    refund = request.form.get("refund_amount", 0, type=int)
    if resolution:
        dispute.admin_resolution = resolution
        dispute.refund_amount = refund or 0
        dispute.status = Dispute.STATUS_RESOLVED
        db.session.commit()
        flash(f"Đã xử lý tranh chấp {dispute.dispute_code}.", "success")
    return redirect(url_for("admin.disputes"))


@admin_bp.route("/payments")
@admin_required
def payments():
    paid = Booking.query.filter_by(payment_status="paid").order_by(
        Booking.created_at.desc()
    ).all()
    pending = Booking.query.filter(
        Booking.payment_status != "paid",
        Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING]),
    ).order_by(Booking.created_at.desc()).all()
    return render_template("admin/payments.html", paid=paid, pending=pending)


@admin_bp.route("/promotions")
@admin_required
def promotions():
    promos = Promotion.query.order_by(Promotion.created_at.desc()).all()
    return render_template("admin/promotions.html", promotions=promos)


@admin_bp.route("/admins")
@admin_required
def admins():
    admins = User.query.filter_by(role="admin").order_by(User.created_at.desc()).all()
    return render_template("admin/admins.html", admins=admins)
