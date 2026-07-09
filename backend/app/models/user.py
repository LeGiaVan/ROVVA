from datetime import datetime
from backend.app.extensions import db

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)
    phone = db.Column(db.String(20))
    id_card = db.Column(db.String(20), nullable=True)
    introduction = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String(255), default="images/host-avatar.png")
    role = db.Column(db.String(20), default="guest") # guest, host, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Auth Status
    is_email_verified = db.Column(db.Boolean, default=False)
    email_verification_token = db.Column(db.String(255), nullable=True)
    reset_password_token = db.Column(db.String(255), nullable=True)
    reset_password_expiry = db.Column(db.DateTime, nullable=True)
    failed_login_attempts = db.Column(db.Integer, default=0)
    is_locked = db.Column(db.Boolean, default=False)
    
    # Host Onboarding Status
    host_status = db.Column(db.String(20), default="none") # none, pending, approved, rejected
    host_document_path = db.Column(db.String(255), nullable=True)

    accommodations = db.relationship("Accommodation", back_populates="host", lazy="dynamic")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.full_name}>"
