from flask import Blueprint, render_template, request

from backend.app.models import Accommodation

accommodation_bp = Blueprint("accommodation", __name__, url_prefix="/accommodations")


@accommodation_bp.route("/")
def index():
    status_filter = request.args.get("status", "all")
    
    query = Accommodation.query
    if status_filter != "all":
        query = query.filter_by(status=status_filter)
        
    accommodations = query.all()
    
    # Get counts for tabs
    counts = {
        "all": Accommodation.query.count(),
        "active": Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE).count(),
        "pending": Accommodation.query.filter_by(status=Accommodation.STATUS_PENDING).count(),
        "paused": Accommodation.query.filter_by(status=Accommodation.STATUS_PAUSED).count(),
        "draft": Accommodation.query.filter_by(status=Accommodation.STATUS_DRAFT).count(),
    }
    
    return render_template(
        "accommodation/index.html",
        active_nav="accommodations",
        accommodations=accommodations,
        current_status=status_filter,
        counts=counts,
    )


@accommodation_bp.route("/<int:id>")
def detail(id):
    from backend.app.models import Room
    acc = Accommodation.query.get_or_404(id)
    status_filter = request.args.get("status", "all")
    
    rooms_query = acc.rooms
    if status_filter != "all":
        rooms_query = rooms_query.filter_by(status=status_filter)
        
    rooms = rooms_query.all()
    
    counts = {
        "all": acc.rooms.count(),
        "active": acc.rooms.filter_by(status=Room.STATUS_ACTIVE).count(),
        "pending": acc.rooms.filter_by(status=Room.STATUS_PENDING).count(),
        "paused": acc.rooms.filter_by(status=Room.STATUS_PAUSED).count(),
        "draft": acc.rooms.filter_by(status=Room.STATUS_DRAFT).count(),
    }
    
    return render_template(
        "accommodation/detail.html",
        active_nav="accommodations",
        acc=acc,
        rooms=rooms,
        current_status=status_filter,
        counts=counts
    )


@accommodation_bp.route("/create", methods=["GET", "POST"])
def create():
    from backend.app.models import User
    from backend.app.extensions import db
    
    # Simulate current user for now
    host = User.query.filter_by(role="host").first()
    
    if request.method == "POST":
        features = request.form.getlist("features")
        
        acc = Accommodation(
            host_id=host.id,
            name=request.form.get("name"),
            type=request.form.get("type"),
            city=request.form.get("city"),
            district=request.form.get("district"),
            address=request.form.get("address"),
            description=request.form.get("description"),
            features=features,
            check_in_time=request.form.get("check_in_time", "14:00"),
            check_out_time=request.form.get("check_out_time", "12:00"),
            cancellation_policy=request.form.get("cancellation_policy"),
            house_rules=request.form.get("house_rules"),
            status=Accommodation.STATUS_PENDING,
            # Hardcode a demo image for now
            image="images/demo-acc.png" 
        )
        db.session.add(acc)
        db.session.commit()
        from flask import redirect, url_for
        return redirect(url_for("accommodation.index"))
        
    return render_template(
        "accommodation/form.html",
        active_nav="accommodations",
        acc=None
    )


@accommodation_bp.route("/<int:id>/edit", methods=["GET", "POST"])
def edit(id):
    from backend.app.extensions import db
    acc = Accommodation.query.get_or_404(id)
    
    if request.method == "POST":
        acc.name = request.form.get("name")
        acc.type = request.form.get("type")
        acc.city = request.form.get("city")
        acc.district = request.form.get("district")
        acc.address = request.form.get("address")
        acc.description = request.form.get("description")
        acc.features = request.form.getlist("features")
        acc.check_in_time = request.form.get("check_in_time", "14:00")
        acc.check_out_time = request.form.get("check_out_time", "12:00")
        acc.cancellation_policy = request.form.get("cancellation_policy")
        acc.house_rules = request.form.get("house_rules")
        
        db.session.commit()
        from flask import redirect, url_for
        return redirect(url_for("accommodation.detail", id=acc.id))
        
    return render_template(
        "accommodation/form.html",
        active_nav="accommodations",
        acc=acc
    )


@accommodation_bp.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    from backend.app.extensions import db
    acc = Accommodation.query.get_or_404(id)
    db.session.delete(acc)
    db.session.commit()
    from flask import redirect, url_for
    return redirect(url_for("accommodation.index"))


# --- ROOM ROUTES ---

@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>")
def room_detail(acc_id, room_id):
    from backend.app.models import Room
    acc = Accommodation.query.get_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc_id).first_or_404()
    
    return render_template(
        "room/detail.html",
        active_nav="accommodations",
        acc=acc,
        room=room
    )


@accommodation_bp.route("/<int:acc_id>/rooms/create", methods=["GET", "POST"])
def room_create(acc_id):
    from backend.app.models import Room
    from backend.app.extensions import db
    
    acc = Accommodation.query.get_or_404(acc_id)
    
    if request.method == "POST":
        features = request.form.getlist("features")
        
        # Simplistic service handling for demo
        services = [
            {"name": "Đưa đón tận nơi", "price": "250000", "unit": "đ/lượt", "checked": True},
            {"name": "Bữa sáng tại sảnh", "price": "150000", "unit": "đ/người/ngày", "checked": True}
        ]
        
        room = Room(
            accommodation_id=acc.id,
            name=request.form.get("name"),
            bed_info=request.form.get("bed_info", "1 Giường đôi"),
            capacity=request.form.get("capacity", 2),
            area=request.form.get("area", "30m2"),
            base_price=request.form.get("base_price", 0),
            description=request.form.get("description"),
            features=features,
            services=services,
            check_in_time=request.form.get("check_in_time", "14:00"),
            check_out_time=request.form.get("check_out_time", "12:00"),
            cancellation_policy=request.form.get("cancellation_policy", "Linh hoạt: Hoàn tiền 100% trước 24h"),
            status=Room.STATUS_PENDING,
            image="images/demo-acc.png"
        )
        db.session.add(room)
        db.session.commit()
        from flask import redirect, url_for
        return redirect(url_for("accommodation.detail", id=acc.id))
        
    return render_template(
        "room/form.html",
        active_nav="accommodations",
        acc=acc,
        room=None
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/edit", methods=["GET", "POST"])
def room_edit(acc_id, room_id):
    from backend.app.models import Room
    from backend.app.extensions import db
    
    acc = Accommodation.query.get_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc_id).first_or_404()
    
    if request.method == "POST":
        room.name = request.form.get("name")
        room.bed_info = request.form.get("bed_info", "1 Giường đôi")
        room.capacity = request.form.get("capacity", 2)
        room.area = request.form.get("area", "30m2")
        room.base_price = request.form.get("base_price", 0)
        room.description = request.form.get("description")
        room.features = request.form.getlist("features")
        room.check_in_time = request.form.get("check_in_time", "14:00")
        room.check_out_time = request.form.get("check_out_time", "12:00")
        room.cancellation_policy = request.form.get("cancellation_policy", "Linh hoạt: Hoàn tiền 100% trước 24h")
        
        db.session.commit()
        from flask import redirect, url_for
        return redirect(url_for("accommodation.room_detail", acc_id=acc.id, room_id=room.id))
        
    return render_template(
        "room/form.html",
        active_nav="accommodations",
        acc=acc,
        room=room
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/pricing")
def room_pricing(acc_id, room_id):
    from backend.app.models import Room
    acc = Accommodation.query.get_or_404(acc_id)
    room = Room.query.filter_by(id=room_id, accommodation_id=acc_id).first_or_404()
    
    return render_template(
        "room/pricing.html",
        active_nav="accommodations",
        acc=acc,
        room=room
    )


@accommodation_bp.route("/<int:acc_id>/rooms/<int:room_id>/delete", methods=["POST"])
def room_delete(acc_id, room_id):
    from backend.app.models import Room
    from backend.app.extensions import db
    
    room = Room.query.filter_by(id=room_id, accommodation_id=acc_id).first_or_404()
    db.session.delete(room)
    db.session.commit()
    from flask import redirect, url_for
    return redirect(url_for("accommodation.detail", id=acc_id))
