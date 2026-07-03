from backend.app.extensions import db


class Accommodation(db.Model):
    __tablename__ = "accommodations"

    STATUS_ACTIVE = "active"
    STATUS_PENDING = "pending"
    STATUS_PAUSED = "paused"
    STATUS_DRAFT = "draft"

    STATUS_LABELS = {
        STATUS_ACTIVE: "Đang hoạt động",
        STATUS_PENDING: "Chờ duyệt",
        STATUS_PAUSED: "Tạm ngừng",
        STATUS_DRAFT: "Bản nháp",
    }

    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), default="Homestay")
    city = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address = db.Column(db.String(500))
    location = db.Column(db.String(200))
    description = db.Column(db.Text)
    image = db.Column(db.String(255))
    status = db.Column(db.String(20), default=STATUS_ACTIVE, nullable=False)
    
    features = db.Column(db.JSON)
    check_in_time = db.Column(db.String(10), default="14:00")
    check_out_time = db.Column(db.String(10), default="12:00")
    cancellation_policy = db.Column(db.String(255), default="Linh hoạt: Hoàn tiền 100% trước 24h")
    house_rules = db.Column(db.Text)

    host = db.relationship("User", back_populates="accommodations")
    rooms = db.relationship(
        "Room", back_populates="accommodation", lazy="dynamic", cascade="all, delete-orphan"
    )

    @property
    def status_label(self):
        return self.STATUS_LABELS.get(self.status, self.status)

    @property
    def total_rooms(self):
        return self.rooms.count()

    @property
    def active_rooms(self):
        return self.rooms.filter_by(status=Room.STATUS_ACTIVE).count()

    @property
    def room_status_text(self):
        return f"{self.active_rooms}/{self.total_rooms} phòng"

    @property
    def occupancy_percent(self):
        if self.total_rooms == 0:
            return 0
        return round(self.active_rooms / self.total_rooms * 100)

    def __repr__(self):
        return f"<Accommodation {self.name}>"


from backend.app.models.room import Room  # noqa: E402
