from datetime import datetime
from backend.app.extensions import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True) # made nullable for now for backwards compat
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(20), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), default="images/host-avatar.png")
    role = db.Column(db.String(20), default="host")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    accommodations = db.relationship("Accommodation", back_populates="host", lazy="dynamic")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.full_name}>"
