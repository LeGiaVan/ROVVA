from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user

from backend.app.models import User
from backend.app.extensions import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role == "host":
            return redirect(url_for("main.index"))
        else:
            return redirect(url_for("customer.index"))
            
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            next_page = request.args.get("next")
            if next_page:
                return redirect(next_page)
            if user.role == "host":
                return redirect(url_for("main.index"))
            else:
                return redirect(url_for("customer.index"))
        flash("Email hoặc mật khẩu không chính xác.", "error")
        
    return render_template("auth/login.html")

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        if current_user.role == "host":
            return redirect(url_for("main.index"))
        else:
            return redirect(url_for("customer.index"))
            
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        # Check if email exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email này đã được sử dụng. Vui lòng đăng nhập hoặc dùng email khác.", "error")
            return redirect(url_for("auth.register"))
            
        if password != confirm_password:
            flash("Mật khẩu xác nhận không khớp.", "error")
            return redirect(url_for("auth.register"))
            
        # Create user
        new_user = User(
            full_name=name,
            email=email,
            phone=phone,
            role="customer"
        )
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for("auth.login"))
        
    return render_template("auth/register.html")

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))
