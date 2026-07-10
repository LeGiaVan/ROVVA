import re
from datetime import datetime, timedelta

from backend.app.models import Conversation, Message, Review
from backend.app.services.host_copilot.context import get_host_rooms

ISSUE_PATTERNS = {
    "noise": {
        "label": "Tiếng ồn / cách âm",
        "keywords": ["ồn", "cách âm", "tiếng động", "đường đông", "inh ỏi"],
        "severity_base": 1.2,
    },
    "damp": {
        "label": "Ẩm mốc / mùi",
        "keywords": ["ẩm", "mốc", "mùi", "thấm", "nồm"],
        "severity_base": 1.3,
    },
    "ac": {
        "label": "Máy lạnh / điều hòa",
        "keywords": ["máy lạnh", "điều hòa", "nóng", "lạnh", "hỏng"],
        "severity_base": 1.1,
    },
    "wifi": {
        "label": "WiFi / mạng",
        "keywords": ["wifi", "mạng", "internet", "sóng", "4g"],
        "severity_base": 0.9,
    },
    "clean": {
        "label": "Vệ sinh",
        "keywords": ["bẩn", "sạch", "vệ sinh", "bụi", "côn trùng"],
        "severity_base": 1.0,
    },
    "water": {
        "label": "Nước / phòng tắm",
        "keywords": ["nước", "yếu", "tắm", "vòi", "bồn"],
        "severity_base": 1.0,
    },
}


def _match_issues(text):
    text_l = (text or "").lower()
    matched = []
    for issue_type, meta in ISSUE_PATTERNS.items():
        for kw in meta["keywords"]:
            if kw in text_l:
                matched.append(issue_type)
                break
    return matched


def _severity(mention_count, avg_rating, days_ago, base):
    recency = max(0.3, 1 - days_ago / 90)
    rating_factor = 1.2 if avg_rating and avg_rating < 4 else 1.0
    return round(mention_count * base * recency * rating_factor, 2)


def scan_maintenance_issues(host_id, resolved_keys=None, days=90):
    resolved_keys = set(resolved_keys or [])
    rooms = get_host_rooms(host_id)
    room_map = {r.id: r for r in rooms}
    cutoff = datetime.utcnow() - timedelta(days=days)

    issues_by_room = {}

    reviews = (
        Review.query.filter(
            Review.room_id.in_(room_map.keys()),
            Review.created_at >= cutoff,
        )
        .order_by(Review.created_at.desc())
        .all()
    )
    for rev in reviews:
        for issue_type in _match_issues(rev.content):
            bucket = issues_by_room.setdefault(rev.room_id, {}).setdefault(
                issue_type,
                {"mentions": [], "ratings": []},
            )
            bucket["mentions"].append(
                {
                    "text": rev.content,
                    "source": "review",
                    "author": rev.guest_name,
                    "rating": rev.rating,
                    "date": rev.created_at,
                }
            )
            bucket["ratings"].append(rev.rating)

    conversations = Conversation.query.filter_by(host_id=host_id).all()
    for conv in conversations:
        messages = (
            Message.query.filter(
                Message.conversation_id == conv.id,
                Message.sender_type == "guest",
                Message.created_at >= cutoff,
            )
            .all()
        )
        for msg in messages:
            matched = _match_issues(msg.content)
            if not matched:
                continue
            for room in rooms:
                if room.accommodation.name.lower() in msg.content.lower() or len(rooms) == 1:
                    target_room_id = room.id
                    break
            else:
                target_room_id = rooms[0].id if rooms else None
            if not target_room_id:
                continue
            for issue_type in matched:
                bucket = issues_by_room.setdefault(target_room_id, {}).setdefault(
                    issue_type,
                    {"mentions": [], "ratings": []},
                )
                bucket["mentions"].append(
                    {
                        "text": msg.content,
                        "source": "message",
                        "author": conv.guest_name,
                        "rating": None,
                        "date": msg.created_at,
                    }
                )

    alerts = []
    for room_id, issue_map in issues_by_room.items():
        room = room_map.get(room_id)
        if not room:
            continue
        for issue_type, data in issue_map.items():
            key = f"{room_id}:{issue_type}"
            if key in resolved_keys:
                continue
            mention_count = len(data["mentions"])
            if mention_count == 0:
                continue
            ratings = [r for r in data["ratings"] if r]
            avg_rating = sum(ratings) / len(ratings) if ratings else 4.0
            latest = data["mentions"][0]["date"]
            days_ago = (datetime.utcnow() - latest).days if latest else 30
            severity = _severity(
                mention_count,
                avg_rating,
                days_ago,
                ISSUE_PATTERNS[issue_type]["severity_base"],
            )
            level = "high" if severity >= 3 else "medium" if severity >= 1.5 else "low"
            alerts.append(
                {
                    "key": key,
                    "room_id": room_id,
                    "room_name": room.name,
                    "acc_name": room.accommodation.name,
                    "issue_type": issue_type,
                    "issue_label": ISSUE_PATTERNS[issue_type]["label"],
                    "mention_count": mention_count,
                    "severity": severity,
                    "level": level,
                    "sample_quote": data["mentions"][0]["text"][:120],
                    "sample_author": data["mentions"][0]["author"],
                    "sample_rating": data["mentions"][0].get("rating"),
                }
            )

    alerts.sort(key=lambda a: a["severity"], reverse=True)
    return alerts[:12]
