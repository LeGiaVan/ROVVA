from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime, timedelta
import uuid

from backend.app.models import Accommodation, Room, Booking
from backend.app.extensions import db

customer_booking_bp = Blueprint("customer_booking", __name__, url_prefix="/customer/booking")

@customer_booking_bp.route("/create/<int:room_id>", methods=["POST"])
@login_required
def create_booking(room_id):
    room = Room.query.get_or_404(room_id)
    
    check_in_str = request.form.get("check_in")
    check_out_str = request.form.get("check_out")
    guest_count = request.form.get("guest_count", 1, type=int)
    guest_note = request.form.get("guest_note", "")
    
    try:
        check_in = datetime.strptime(check_in_str, "%Y-%m-%d").date()
        check_out = datetime.strptime(check_out_str, "%Y-%m-%d").date()
    except (ValueError, TypeError):
        flash("Ngày check-in hoặc check-out không hợp lệ.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))
        
    if check_in >= check_out:
        flash("Ngày trả phòng phải sau ngày nhận phòng.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))
        
    # Check for overlapping bookings (confirmed or holding)
    overlap = Booking.query.filter(
        Booking.room_id == room_id,
        Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING]),
        Booking.check_in < check_out,
        Booking.check_out > check_in
    ).first()
    
    # Also we should clear expired holdings before checking ideally, but we can also just filter them
    if overlap and overlap.status == Booking.STATUS_HOLDING and overlap.hold_expiry_at and overlap.hold_expiry_at < datetime.utcnow():
        # It's an expired hold, we can ignore it (or mark as cancelled)
        overlap.status = Booking.STATUS_CANCELLED
        db.session.commit()
    elif overlap:
        flash("Phòng đã được đặt hoặc đang có người giữ chỗ trong khoảng thời gian này.", "error")
        return redirect(url_for("customer.accommodation_detail", id=room.accommodation_id))
        
    nights = (check_out - check_in).days
    total_amount = room.base_price * nights # simplified pricing
    
    booking_code = f"#RV{uuid.uuid4().hex[:6].upper()}"
    
    booking = Booking(
        booking_code=booking_code,
        room_id=room_id,
        guest_id=current_user.id,
        guest_name=current_user.full_name,
        guest_phone=current_user.phone,
        guest_email=current_user.email,
        guest_count=guest_count,
        guest_note=guest_note,
        check_in=check_in,
        check_out=check_out,
        total_amount=total_amount,
        status=Booking.STATUS_HOLDING,
        hold_expiry_at=datetime.utcnow() + timedelta(minutes=15) # Hold for 15 minutes
    )
    
    db.session.add(booking)
    db.session.commit()
    
    return redirect(url_for("customer_booking.checkout", booking_code=booking_code))

@customer_booking_bp.route("/checkout/<booking_code>", methods=["GET", "POST"])
@login_required
def checkout(booking_code):
    booking = Booking.query.filter_by(booking_code=booking_code, guest_id=current_user.id).first_or_404()
    
    if booking.status != Booking.STATUS_HOLDING:
        flash("Booking này không ở trạng thái chờ thanh toán.", "warning")
        return redirect(url_for("customer.index"))
        
    if booking.hold_expiry_at and booking.hold_expiry_at < datetime.utcnow():
        booking.status = Booking.STATUS_CANCELLED
        db.session.commit()
        flash("Thời gian giữ chỗ đã hết hạn. Vui lòng đặt lại.", "error")
        return redirect(url_for("customer.index"))
        
    if request.method == "POST":
        payment_method = request.form.get("payment_method")
        
        if payment_method == "cash":
            booking.status = Booking.STATUS_CONFIRMED
            booking.payment_method = "cash"
            booking.commission_fee = int(booking.total_amount * 0.15) # 15% commission
            booking.host_payout_amount = booking.total_amount - booking.commission_fee
            db.session.commit()
            flash("Đặt phòng thành công! Bạn sẽ thanh toán bằng tiền mặt khi nhận phòng.", "success")
            return redirect(url_for("customer.index"))
            
        elif payment_method == "online":
            # Mock redirect to payment gateway
            return redirect(url_for("customer_booking.mock_gateway", booking_code=booking_code))
            
    return render_template("customer/pages/checkout.html", booking=booking)

@customer_booking_bp.route("/mock-gateway/<booking_code>")
@login_required
def mock_gateway(booking_code):
    booking = Booking.query.filter_by(booking_code=booking_code, guest_id=current_user.id).first_or_404()
    return render_template("customer/pages/mock_payment.html", booking=booking)

@customer_booking_bp.route("/payment-callback/<booking_code>")
@login_required
def payment_callback(booking_code):
    booking = Booking.query.filter_by(booking_code=booking_code, guest_id=current_user.id).first_or_404()
    
    status = request.args.get("status")
    if status == "success":
        booking.status = Booking.STATUS_CONFIRMED
        booking.payment_status = "paid"
        booking.payment_method = "online"
        booking.payment_gateway_ref = f"TXN{uuid.uuid4().hex[:8].upper()}"
        booking.commission_fee = int(booking.total_amount * 0.15)
        booking.host_payout_amount = booking.total_amount - booking.commission_fee
        db.session.commit()
        flash("Thanh toán thành công! Chúc bạn có kỳ nghỉ vui vẻ.", "success")
    else:
        flash("Thanh toán thất bại hoặc bị hủy.", "error")
        
    return redirect(url_for("customer.index"))
