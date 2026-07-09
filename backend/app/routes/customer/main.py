from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")

@customer_bp.route("/")
def index():
    from flask_login import current_user
    from backend.app.models import Accommodation
    
    featured_hotels = Accommodation.query.filter_by(status='active').filter(Accommodation.type.in_(['KhÃ¡ch sáº¡n', 'Resort'])).limit(4).all()
    featured_apartments = Accommodation.query.filter_by(status='active').filter(Accommodation.type.in_(['CÄƒn há»™', 'Homestay'])).limit(4).all()
    
    try:
        if current_user.is_authenticated and current_user.role in ['customer', 'guest']:
            return render_template("customer/pages/home/member.html", 
                                   featured_hotels=featured_hotels, 
                                   featured_apartments=featured_apartments)
        else:
            return render_template("customer/pages/home/guest.html",
                                   featured_hotels=featured_hotels, 
                                   featured_apartments=featured_apartments)
    except TemplateNotFound:
        abort(404)

@customer_bp.route("/accommodation/<int:id>")
def accommodation_detail(id):
    from backend.app.models import Accommodation
    acc = Accommodation.query.get_or_404(id)
    return render_template("customer/pages/accommodation/detail.html", acc=acc)

@customer_bp.route("/become-host", methods=["GET", "POST"])
@login_required
def become_host():
    if current_user.role == "host":
        return redirect(url_for("main.index"))
        
    if current_user.host_status == "pending":
        flash("Hồ sơ đăng ký của bạn đang được duyệt. Vui lòng chờ phản hồi từ ban quản trị.", "info")
        return redirect(url_for("customer.index"))
        
    if request.method == "POST":
        id_card = request.form.get("id_card")
        document_path = request.form.get("document_path") # Giả lập đường dẫn upload file
        
        current_user.id_card = id_card
        current_user.host_document_path = document_path
        current_user.host_status = "pending"
        
        from backend.app.extensions import db
        db.session.commit()
        
        flash("Đăng ký thành công! Hồ sơ của bạn đang được xét duyệt.", "success")
        return redirect(url_for("customer.index"))
        
    return render_template("customer/pages/host_registration.html")

@customer_bp.route("/<path:page_path>")
def show_page(page_path):
    if ".." in page_path:
        abort(400)
    try:
        return render_template(f"customer/{page_path}")
    except TemplateNotFound:
        abort(404)
