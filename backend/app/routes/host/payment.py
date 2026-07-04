from flask import Blueprint, render_template, request, redirect, url_for, flash
from sqlalchemy import func
from backend.app.models import Booking, Withdrawal, User, Accommodation, Dispute
from backend.app.extensions import db

payment_bp = Blueprint("payment", __name__, url_prefix="/payments")

@payment_bp.route("/")
def index():
    status_filter = request.args.get("status", "Tất cả")
    page = request.args.get('page', 1, type=int)
    per_page = 10

    host_id = 1 # Assuming single host or logged in user's ID
    
    # 1. Thống kê
    # Pending Revenue
    pending_bookings = Booking.query.filter_by(payment_status="pending").all()
    pending_revenue = sum([b.total_amount * 0.9 for b in pending_bookings])
    
    # In Dispute Amount
    dispute_bookings = Booking.query.filter_by(payment_status="in_dispute").all()
    in_dispute_amount = sum([b.total_amount * 0.9 for b in dispute_bookings])
    
    # Total Disbursed (from platform to host wallet)
    disbursed_bookings = Booking.query.filter_by(payment_status="disbursed").all()
    total_disbursed_to_wallet = sum([b.total_amount * 0.9 for b in disbursed_bookings])
    
    # Withdrawals
    withdrawals = Withdrawal.query.all() # In reality, filter by host_id
    total_withdrawn = sum([w.amount for w in withdrawals if w.status == Withdrawal.STATUS_COMPLETED])
    total_pending_withdraw = sum([w.amount for w in withdrawals if w.status == Withdrawal.STATUS_PENDING])
    
    # Withdrawable balance
    withdrawable_balance = total_disbursed_to_wallet - total_withdrawn - total_pending_withdraw
    
    # 2. Lấy danh sách giao dịch (Transactions)
    query = Booking.query
    if status_filter == "Chờ giải ngân":
        query = query.filter(Booking.payment_status == "pending")
    elif status_filter == "Đang tranh chấp":
        query = query.filter(Booking.payment_status == "in_dispute")
    elif status_filter == "Đã giải ngân":
        query = query.filter(Booking.payment_status == "disbursed")
    elif status_filter == "Đã giải quyết":
        query = query.filter(Booking.payment_status == "resolved")
        
    pagination = query.order_by(Booking.created_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
    
    # Lấy danh sách cơ sở lưu trú cho bộ lọc
    accommodations = Accommodation.query.all()
    
    return render_template(
        "host/payment/index.html",
        active_nav="payments",
        active_tab=status_filter,
        pagination=pagination,
        pending_revenue=int(pending_revenue),
        withdrawable_balance=int(withdrawable_balance),
        in_dispute_amount=int(in_dispute_amount),
        total_withdrawn=int(total_withdrawn),
        accommodations=accommodations
    )

@payment_bp.route("/withdraw", methods=["POST"])
def withdraw():
    amount_str = request.form.get("amount")
    
    try:
        # Xóa dấu chấm hoặc phẩy và convert sang int
        amount = int(amount_str.replace('.', '').replace(',', ''))
        
        # Hardcode bank cho demo
        bank_account = "Vietcombank xxxx 1234"
        
        withdrawal = Withdrawal(
            host_id=1, # Hardcode host_id
            amount=amount,
            bank_account=bank_account,
            status=Withdrawal.STATUS_COMPLETED # Giả lập rút thành công luôn
        )
        db.session.add(withdrawal)
        db.session.commit()
        
        flash(f"Đã đặt lệnh rút thành công {amount:,.0f} đ", "success")
    except ValueError:
        flash("Số tiền không hợp lệ", "danger")
        
    return redirect(url_for("payment.index"))
