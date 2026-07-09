from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from backend.app.models import User, Accommodation
from backend.app.extensions import db
from backend.app.routes.admin import admin_bp

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "admin":
            flash("Bạn không có quyền truy cập trang này.", "error")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route("/")
@admin_required
def index():
    return render_template("admin/index.html")

@admin_bp.route("/hosts")
@admin_required
def hosts():
    pending_hosts = User.query.filter_by(host_status="pending").all()
    approved_hosts = User.query.filter_by(role="host").all()
    return render_template("admin/hosts.html", pending=pending_hosts, approved=approved_hosts)

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
    pending_accs = Accommodation.query.filter_by(status=Accommodation.STATUS_PENDING).all()
    return render_template("admin/accommodations.html", pending=pending_accs)

@admin_bp.route("/accommodations/<int:acc_id>/approve", methods=["POST"])
@admin_required
def approve_accommodation(acc_id):
    acc = Accommodation.query.get_or_404(acc_id)
    if acc.status == Accommodation.STATUS_PENDING:
        acc.status = Accommodation.STATUS_ACTIVE
        db.session.commit()
        flash(f"Đã duyệt chỗ nghỉ: {acc.name}", "success")
    return redirect(url_for("admin.accommodations"))
