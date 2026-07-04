from flask import Blueprint, render_template, abort
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

@customer_bp.route("/<path:page_path>")
def show_page(page_path):
    if ".." in page_path:
        abort(400)
    try:
        return render_template(f"customer/{page_path}")
    except TemplateNotFound:
        abort(404)
