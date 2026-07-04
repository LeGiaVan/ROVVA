from backend.app.extensions import db
from datetime import datetime

class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    type = db.Column(db.String(50), nullable=False) # earn, spend
    amount = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('wallet_transactions', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<WalletTransaction {self.type} {self.amount} for User {self.user_id}>'
