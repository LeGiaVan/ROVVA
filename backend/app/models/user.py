from backend.app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    avatar = db.Column(db.String(255), default="images/host-avatar.png")
    role = db.Column(db.String(20), default="host")

    accommodations = db.relationship("Accommodation", back_populates="host", lazy="dynamic")

    def __repr__(self):
        return f"<User {self.full_name}>"
