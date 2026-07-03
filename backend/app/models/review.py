from datetime import datetime
from backend.app.extensions import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    room_id = db.Column(db.Integer, db.ForeignKey("rooms.id"), nullable=False)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_avatar = db.Column(db.String(255))
    booking_code = db.Column(db.String(50))
    rating = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    reply_at = db.Column(db.DateTime)

    room = db.relationship("Room", backref="reviews")
