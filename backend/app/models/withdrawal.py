from datetime import datetime

from backend.app.extensions import db

class Withdrawal(db.Model):
    __tablename__ = "withdrawals"

    STATUS_PENDING = "pending"
    STATUS_COMPLETED = "completed"

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    bank_account = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default=STATUS_PENDING, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)

    host = db.relationship("User", backref=db.backref("withdrawals", lazy=True))

    def __repr__(self):
        return f"<Withdrawal #{self.id} {self.amount}>"
