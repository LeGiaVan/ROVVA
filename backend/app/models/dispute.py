from datetime import datetime
from backend.app.extensions import db

class Dispute(db.Model):
    __tablename__ = "disputes"

    STATUS_NEEDS_RESPONSE = "needs_response"
    STATUS_PROCESSING = "processing"
    STATUS_RESOLVED = "resolved"

    id = db.Column(db.Integer, primary_key=True)
    dispute_code = db.Column(db.String(20), unique=True, index=True, nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)
    status = db.Column(db.String(20), default=STATUS_NEEDS_RESPONSE, nullable=False)
    
    # Guest Complaint
    guest_complaint = db.Column(db.Text, nullable=False)
    guest_evidence = db.Column(db.Text) # JSON serialized list of image URLs
    
    # Host Response
    host_response = db.Column(db.Text)
    host_evidence = db.Column(db.Text) # JSON serialized list of image URLs
    
    # Admin Resolution
    admin_resolution = db.Column(db.Text)
    refund_amount = db.Column(db.Integer, default=0)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    booking = db.relationship("Booking", backref=db.backref("disputes", lazy=True))

    def __repr__(self):
        return f"<Dispute #{self.dispute_code}>"
