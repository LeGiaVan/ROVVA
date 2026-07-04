from backend.app.extensions import db
from datetime import datetime

class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    accommodation_id = db.Column(db.Integer, db.ForeignKey('accommodations.id'), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship('User', backref=db.backref('favorites', lazy=True, cascade="all, delete-orphan"))
    accommodation = db.relationship('Accommodation', backref=db.backref('favorited_by', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f'<Favorite User {self.user_id} -> Acc {self.accommodation_id}>'
