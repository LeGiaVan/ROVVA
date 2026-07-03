from datetime import datetime
from backend.app.extensions import db


class Promotion(db.Model):
    __tablename__ = "promotions"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Giảm %, Giảm cố định
    discount_value = db.Column(db.String(50))  # e.g., "20", "100000"
    start_date = db.Column(db.String(20))
    end_date = db.Column(db.String(20))
    min_nights = db.Column(db.Integer, default=1)
    apply_days = db.Column(db.String(50))  # e.g., "Thứ 2 - Thứ 5"
    not_combine = db.Column(db.Boolean, default=False)
    applied_to = db.Column(db.JSON)  # To mock tree selection
    status = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    host = db.relationship("User", backref="promotions")
