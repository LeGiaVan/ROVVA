from datetime import datetime

from backend.app.extensions import db


class Booking(db.Model):
    __tablename__ = "bookings"

    STATUS_CONFIRMED = "confirmed"
    STATUS_PENDING = "pending"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"

    id = db.Column(db.Integer, primary_key=True)
    booking_code = db.Column(db.String(20), unique=True, index=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    guest_name = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20))
    guest_email = db.Column(db.String(120))
    guest_count = db.Column(db.Integer, default=1)
    guest_note = db.Column(db.Text)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    total_amount = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default=STATUS_CONFIRMED, nullable=False)
    payment_status = db.Column(db.String(20), default="pending", nullable=False) # pending, disbursed, in_dispute, resolved
    disbursed_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    room = db.relationship("Room", back_populates="bookings")

    @property
    def nights(self):
        return (self.check_out - self.check_in).days

    def __repr__(self):
        return f"<Booking #{self.id} {self.guest_name}>"
