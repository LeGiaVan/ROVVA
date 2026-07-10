from flask import Blueprint, render_template, abort, request, flash, redirect, url_for
from flask_login import login_required, current_user
from jinja2 import TemplateNotFound

customer_bp = Blueprint("customer", __name__, url_prefix="/customer")

HOTEL_TYPES = ["Khách sạn", "Resort"]
APARTMENT_TYPES = ["Căn hộ", "Homestay", "Villa", "Cottage"]


def _trending_destinations(limit=4):
    """Nhóm các CSLT đang hoạt động theo thành phố, chọn top theo số lượng."""
    from backend.app.models import Accommodation

    active = Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE).all()
    by_city = {}
    for acc in active:
        city = (acc.city or "").strip() or "Việt Nam"
        by_city.setdefault(city, []).append(acc)

    destinations = []
    for city, accs in by_city.items():
        destinations.append({
            "city": city,
            "count": len(accs),
            "cover_url": accs[0].cover_url,
        })
    destinations.sort(key=lambda d: d["count"], reverse=True)
    return destinations[:limit]


@customer_bp.route("/")
def index():
    from backend.app.models import Accommodation

    featured_hotels = (
        Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE)
        .filter(Accommodation.type.in_(HOTEL_TYPES))
        .limit(4)
        .all()
    )
    featured_apartments = (
        Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE)
        .filter(Accommodation.type.in_(APARTMENT_TYPES))
        .limit(4)
        .all()
    )
    trending = _trending_destinations()

    context = {
        "featured_hotels": featured_hotels,
        "featured_apartments": featured_apartments,
        "trending": trending,
    }

    try:
        if current_user.is_authenticated and current_user.role in ["customer", "guest"]:
            return render_template("customer/pages/home/member.html", **context)
        return render_template("customer/pages/home/guest.html", **context)
    except TemplateNotFound:
        abort(404)

@customer_bp.route("/accommodation/<int:id>")
def accommodation_detail(id):
    from backend.app.models import Accommodation, Review, Room

    acc = Accommodation.query.get_or_404(id)
    reviews = (
        Review.query.join(Room)
        .filter(Room.accommodation_id == acc.id)
        .order_by(Review.created_at.desc())
        .limit(6)
        .all()
    )
    return render_template(
        "customer/pages/accommodation/detail.html", acc=acc, reviews=reviews
    )

@customer_bp.route("/become-host", methods=["GET", "POST"])
@login_required
def become_host():
    if current_user.role == "host":
        return redirect(url_for("main.index"))
        
    if current_user.host_status == "pending":
        flash("Hồ sơ đăng ký của bạn đang được duyệt. Vui lòng chờ phản hồi từ ban quản trị.", "info")
        return redirect(url_for("customer.index"))
        
    if request.method == "POST":
        id_card = request.form.get("id_card")
        document_path = request.form.get("document_path") # Giả lập đường dẫn upload file
        
        current_user.id_card = id_card
        current_user.host_document_path = document_path
        current_user.host_status = "pending"
        
        from backend.app.extensions import db
        db.session.commit()
        
        flash("Đăng ký thành công! Hồ sơ của bạn đang được xét duyệt.", "success")
        return redirect(url_for("customer.index"))
        
    return render_template("customer/pages/host_registration.html")

ACCOMMODATION_TYPES = ["Khách sạn", "Homestay", "Căn hộ", "Resort", "Villa", "Cottage"]

CANCELLATION_OPTIONS = ["Hủy miễn phí", "Hủy có phí", "Không cho hủy"]

AMENITY_OPTIONS = [
    "Sân vườn", "Hồ bơi", "Bãi đậu xe", "Thang máy", "Wifi",
    "Phòng tập thể hình", "Máy lạnh", "Ban công", "Bồn tắm", "Cho phép thú cưng",
]


def _acc_amenities_text(acc):
    """Gộp toàn bộ tiện ích của CSLT + phòng thành 1 chuỗi thường để dò filter."""
    parts = list(acc.features or [])
    for room in acc.rooms:
        parts.extend(room.features or [])
        for s in (room.services or []):
            if isinstance(s, dict):
                parts.append(s.get("name", ""))
            else:
                parts.append(str(s))
    return " ".join(str(p) for p in parts).lower()


@customer_bp.route("/search")
def search():
    from backend.app.models import Accommodation
    from backend.app.extensions import db

    args = request.args
    location = (args.get("location") or "").strip()
    price_min = args.get("price_min", type=int)
    price_max = args.get("price_max", type=int)
    types = [t for t in args.getlist("type") if t]
    guests = args.get("guests", type=int)
    amenities = [a for a in args.getlist("amenity") if a]
    sort = args.get("sort", "recommended")

    query = Accommodation.query.filter_by(status=Accommodation.STATUS_ACTIVE)

    if location:
        like = f"%{location}%"
        query = query.filter(
            db.or_(
                Accommodation.city.ilike(like),
                Accommodation.location.ilike(like),
                Accommodation.name.ilike(like),
                Accommodation.address.ilike(like),
            )
        )
    if types:
        query = query.filter(Accommodation.type.in_(types))

    candidates = query.all()

    # Lọc theo giá / sức chứa / tiện ích (dựa trên phòng + JSON) bằng Python.
    results = []
    for acc in candidates:
        price = acc.min_price
        max_capacity = max([r.capacity or 0 for r in acc.rooms.filter_by(status="active")], default=0)

        if price_min is not None and price and price < price_min:
            continue
        if price_max is not None and price and price > price_max:
            continue
        if guests and max_capacity < guests:
            continue
        if amenities:
            haystack = _acc_amenities_text(acc)
            if not all(a.lower() in haystack for a in amenities):
                continue
        results.append(acc)

    if sort == "price_asc":
        results.sort(key=lambda a: a.min_price or 0)
    elif sort == "price_desc":
        results.sort(key=lambda a: a.min_price or 0, reverse=True)
    elif sort == "rating":
        results.sort(key=lambda a: a.average_rating or 0, reverse=True)

    selected = {
        "location": location,
        "price_min": price_min,
        "price_max": price_max,
        "types": types,
        "guests": guests,
        "amenities": amenities,
        "sort": sort,
    }

    return render_template(
        "customer/pages/home/search-results.html",
        results=results,
        selected=selected,
        type_options=ACCOMMODATION_TYPES,
        amenity_options=AMENITY_OPTIONS,
        cancellation_options=CANCELLATION_OPTIONS,
    )


@customer_bp.route("/smart-search")
def smart_search():
    from backend.app.models import Room
    from backend.app.services.smart_match import smart_match
    from sqlalchemy.orm import joinedload

    query = request.args.get("q", "").strip()
    results = []
    error = None

    if query:
        try:
            matches = smart_match(query, top_n=6)
        except Exception:  # noqa: BLE001 - tránh 500 nếu DB/model lỗi
            matches = []
            error = "Không thể chạy Smart Match lúc này. Vui lòng thử lại."

        if matches:
            ids = [m["room_id"] for m in matches]
            rooms = (
                Room.query.filter(Room.id.in_(ids))
                .options(joinedload(Room.accommodation))
                .all()
            )
            room_by_id = {r.id: r for r in rooms}
            for m in matches:
                room = room_by_id.get(m["room_id"])
                if room:
                    results.append({
                        "room": room,
                        "score": m["score"],
                        "rating": m.get("rating", 0),
                        "reasons": m.get("reasons", []),
                    })

    return render_template(
        "customer/pages/home/smart-results.html",
        query=query,
        results=results,
        error=error,
    )


def _member_tier(user):
    from backend.app.models import Booking

    if not getattr(user, "is_authenticated", False):
        return {"label": "Khách", "cls": "account-sidebar__tier--silver"}
    completed = Booking.query.filter_by(
        guest_id=user.id, status=Booking.STATUS_COMPLETED
    ).count()
    if completed >= 5:
        return {"label": "Hạng Bạch Kim", "cls": "account-sidebar__tier--platinum"}
    if completed >= 2:
        return {"label": "Hạng Vàng", "cls": ""}
    return {"label": "Hạng Bạc", "cls": "account-sidebar__tier--silver"}


@customer_bp.app_context_processor
def inject_member_tier():
    return {"member_tier": _member_tier(current_user)}


def _wallet_balance(user_id):
    from backend.app.models import WalletTransaction

    txs = WalletTransaction.query.filter_by(user_id=user_id).all()
    balance = sum(t.amount if t.type == "earn" else -t.amount for t in txs)
    return balance, txs


@customer_bp.route("/account/profile", methods=["GET", "POST"])
@login_required
def account_profile():
    from backend.app.extensions import db
    from datetime import datetime

    if request.method == "POST":
        current_user.full_name = request.form.get("name") or current_user.full_name
        current_user.phone = request.form.get("phone") or current_user.phone
        current_user.gender = request.form.get("gender") or current_user.gender
        current_user.city = request.form.get("city") or current_user.city
        birthday = request.form.get("birthday")
        if birthday:
            try:
                current_user.birthday = datetime.strptime(birthday, "%Y-%m-%d").date()
            except ValueError:
                pass
        db.session.commit()
        flash("Đã cập nhật hồ sơ.", "success")
        return redirect(url_for("customer.account_profile"))

    return render_template("customer/pages/account/profile.html")


@customer_bp.route("/trips")
@login_required
def trips():
    from backend.app.models import Booking

    tab = request.args.get("tab", "upcoming")
    base = Booking.query.filter_by(guest_id=current_user.id)

    if tab == "completed":
        bookings = base.filter_by(status=Booking.STATUS_COMPLETED)
    elif tab == "cancelled":
        bookings = base.filter_by(status=Booking.STATUS_CANCELLED)
    else:
        tab = "upcoming"
        bookings = base.filter(
            Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING, Booking.STATUS_PENDING])
        )

    bookings = bookings.order_by(Booking.check_in.desc()).all()

    counts = {
        "upcoming": base.filter(Booking.status.in_([Booking.STATUS_CONFIRMED, Booking.STATUS_HOLDING, Booking.STATUS_PENDING])).count(),
        "completed": base.filter_by(status=Booking.STATUS_COMPLETED).count(),
        "cancelled": base.filter_by(status=Booking.STATUS_CANCELLED).count(),
    }

    return render_template(
        "customer/pages/trip/upcoming.html", bookings=bookings, tab=tab, counts=counts
    )


@customer_bp.route("/account/wallet")
@login_required
def account_wallet():
    balance, txs = _wallet_balance(current_user.id)
    txs = sorted(txs, key=lambda t: t.created_at or 0, reverse=True)
    return render_template(
        "customer/pages/account/wallet.html", balance=balance, transactions=txs
    )


@customer_bp.route("/account/favorites")
@login_required
def account_favorites():
    from backend.app.models import Favorite

    favorites = Favorite.query.filter_by(user_id=current_user.id).all()
    accommodations = [f.accommodation for f in favorites if f.accommodation]
    return render_template(
        "customer/pages/account/favorites.html", accommodations=accommodations
    )


@customer_bp.route("/account/reviews")
@login_required
def account_reviews():
    from backend.app.models import Booking

    completed = (
        Booking.query.filter_by(guest_id=current_user.id, status=Booking.STATUS_COMPLETED)
        .order_by(Booking.check_out.desc())
        .all()
    )
    return render_template(
        "customer/pages/account/reviews-pending.html", completed=completed
    )


@customer_bp.route("/account/security")
@login_required
def account_security():
    return render_template("customer/pages/account/security.html")


@customer_bp.route("/account/tier")
@login_required
def account_tier():
    balance, _ = _wallet_balance(current_user.id)
    return render_template("customer/pages/account/tier.html", balance=balance)


# Các template dưới đây được render qua route riêng (cần context/đăng nhập),
# không cho phép truy cập trực tiếp qua catch-all để tránh lỗi thiếu dữ liệu.
_SSR_ONLY_PREFIXES = ("pages/account/", "pages/trip/")

_SSR_REDIRECTS = {
    "pages/home/guest.html": "customer.index",
    "pages/home/member.html": "customer.index",
    "pages/auth/login.html": "auth.login",
    "pages/auth/register.html": "auth.register",
    "pages/account/profile.html": "customer.account_profile",
    "pages/account/wallet.html": "customer.account_wallet",
    "pages/account/favorites.html": "customer.account_favorites",
    "pages/account/security.html": "customer.account_security",
    "pages/account/tier.html": "customer.account_tier",
    "pages/account/reviews-pending.html": "customer.account_reviews",
    "pages/account/reviews-completed.html": "customer.account_reviews",
    "pages/trip/upcoming.html": "customer.trips",
}


@customer_bp.route("/chat")
def ai_chat():
    if current_user.is_authenticated and current_user.role in ("customer", "guest"):
        return render_template("customer/pages/chat/member.html")
    return render_template("customer/pages/chat/guest.html")


@customer_bp.route("/<path:page_path>")
def show_page(page_path):
    if ".." in page_path:
        abort(400)

    if page_path in ("pages/chat/guest.html", "pages/chat/member.html"):
        return redirect(url_for("customer.ai_chat"))

    if page_path in _SSR_REDIRECTS:
        return redirect(url_for(_SSR_REDIRECTS[page_path]))
    if page_path.startswith(_SSR_ONLY_PREFIXES):
        return redirect(url_for("customer.account_profile"))

    try:
        return render_template(f"customer/{page_path}")
    except TemplateNotFound:
        abort(404)
