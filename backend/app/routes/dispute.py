from flask import Blueprint, render_template, request, redirect, url_for, flash
from backend.app.models import Dispute, Booking
from backend.app.extensions import db

dispute_bp = Blueprint("dispute", __name__, url_prefix="/disputes")

@dispute_bp.route("/")
def index():
    status_filter = request.args.get("status", "Tất cả")
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    query = Dispute.query
    
    if status_filter == "Đang xử lý":
        query = query.filter(Dispute.status == Dispute.STATUS_PROCESSING)
    elif status_filter == "Cần phản hồi":
        query = query.filter(Dispute.status == Dispute.STATUS_NEEDS_RESPONSE)
    elif status_filter == "Đã giải quyết":
        query = query.filter(Dispute.status == Dispute.STATUS_RESOLVED)
        
    pagination = query.order_by(Dispute.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    needs_response_count = Dispute.query.filter_by(status=Dispute.STATUS_NEEDS_RESPONSE).count()
    
    return render_template(
        "dispute/index.html",
        active_nav="disputes",
        active_tab=status_filter,
        pagination=pagination,
        needs_response_count=needs_response_count
    )

@dispute_bp.route("/<int:id>")
def detail(id):
    dispute = Dispute.query.get_or_404(id)
    return render_template(
        "dispute/detail.html",
        active_nav="disputes",
        dispute=dispute
    )

@dispute_bp.route("/<int:id>/respond", methods=["POST"])
def respond(id):
    dispute = Dispute.query.get_or_404(id)
    
    response_content = request.form.get("response_content")
    
    if response_content:
        dispute.host_response = response_content
        dispute.status = Dispute.STATUS_PROCESSING
        db.session.commit()
        flash("Phản hồi của bạn đã được hệ thống ghi nhận.", "success")
        
    return redirect(url_for("dispute.detail", id=id))
