"""Smart Match - Core logic gợi ý phòng bằng TF-IDF + Cosine Similarity.

Nhận vào một chuỗi mô tả nhu cầu bằng ngôn ngữ tự nhiên
(vd: "phòng cho 2 người có hồ bơi"), đọc dữ liệu Room/Accommodation
từ SQLite bằng Pandas, và trả về top N phòng phù hợp nhất.

Đây là phần CORE LOGIC (chưa gồm API/UI). Có thể chạy trực tiếp:
    python -m backend.app.services.smart_match "phòng cho 2 người có hồ bơi"
"""

import json
import os
import re
import sqlite3

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Trọng số kết hợp: độ tương đồng ngữ nghĩa vs điểm đánh giá thực tế.
_WEIGHT_SIMILARITY = 0.85
_WEIGHT_RATING = 0.15

# Từ quá phổ biến -> bỏ qua khi dò 'lý do gợi ý' để tránh nhiễu.
_STOPWORDS = {
    "phòng", "có", "và", "ở", "cho", "các", "một", "gần", "tôi", "cần",
    "muốn", "với", "người", "khách", "đêm", "giá", "dưới", "trên", "là",
    "ngày", "chỗ", "nơi", "đi", "the", "a", "an", "room",
}

# instance/rova_host.db nằm ở thư mục gốc dự án (services -> app -> backend -> root)
_DEFAULT_DB_PATH = os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "instance", "rova_host.db"
)


def _parse_json_items(value):
    """Trả về list nhãn từ cột JSON. Với phần tử là dict (vd service có
    name/price/unit) chỉ lấy trường 'name' để tránh nhiễu khi khớp/hiển thị."""
    if not value:
        return []
    try:
        data = json.loads(value) if isinstance(value, str) else value
    except (ValueError, TypeError):
        return [str(value)]
    if isinstance(data, dict):
        data = list(data.values())
    if not isinstance(data, (list, tuple)):
        return [str(data)]

    items = []
    for el in data:
        if isinstance(el, dict):
            label = el.get("name") or el.get("label") or el.get("title")
            if label:
                items.append(str(label))
        elif el:
            items.append(str(el))
    return items


def _parse_json_list(value):
    """Chuỗi text an toàn từ cột JSON (dùng cho corpus TF-IDF)."""
    return " ".join(_parse_json_items(value))


def load_rooms_dataframe(db_path=None):
    """Đọc dữ liệu phòng (join với accommodation) từ SQLite bằng Pandas."""
    db_path = os.path.abspath(db_path or _DEFAULT_DB_PATH)
    if not os.path.exists(db_path):
        raise FileNotFoundError(f"Không tìm thấy database SQLite tại: {db_path}")

    query = """
        SELECT
            r.id                AS room_id,
            r.name              AS room_name,
            r.bed_info          AS bed_info,
            r.capacity          AS capacity,
            r.area              AS area,
            r.base_price        AS base_price,
            r.description       AS room_description,
            r.features          AS room_features,
            r.services          AS room_services,
            a.id                AS accommodation_id,
            a.name              AS accommodation_name,
            a.type              AS accommodation_type,
            a.city              AS city,
            a.district          AS district,
            a.description       AS accommodation_description,
            a.features          AS accommodation_features,
            a.allows_pets       AS allows_pets,
            (SELECT AVG(rv.rating) FROM reviews rv WHERE rv.room_id = r.id) AS avg_rating
        FROM rooms r
        JOIN accommodations a ON r.accommodation_id = a.id
        WHERE r.status = 'active' AND a.status = 'active'
    """

    conn = sqlite3.connect(db_path)
    try:
        df = pd.read_sql_query(query, conn)
    finally:
        conn.close()
    return df


def _build_reasons(row, query, max_reasons=4):
    """Sinh danh sách 'lý do gợi ý' bằng cách khớp truy vấn với dữ liệu phòng."""
    q = (query or "").lower()
    query_tokens = set(re.findall(r"\w+", q)) - _STOPWORDS
    reasons = []

    def _matches(text):
        text_tokens = set(re.findall(r"\w+", str(text).lower()))
        return bool(text_tokens & query_tokens)

    # Tiện ích & dịch vụ (accommodation + room) khớp với truy vấn.
    amenities = (
        _parse_json_items(row.get("accommodation_features"))
        + _parse_json_items(row.get("room_features"))
        + _parse_json_items(row.get("room_services"))
    )
    seen = set()
    for item in amenities:
        key = item.lower().strip()
        if key and key not in seen and _matches(item):
            reasons.append(item)
            seen.add(key)

    # Địa điểm.
    for field in ("city", "district"):
        val = row.get(field)
        if val and _matches(val) and val not in reasons:
            reasons.append(val)

    # Sức chứa: nếu truy vấn nhắc tới đúng con số khách.
    capacity = int(row.get("capacity") or 0)
    numbers = {int(n) for n in re.findall(r"\d+", q)}
    if capacity and capacity in numbers:
        reasons.append(f"{capacity} khách")

    # Thú cưng.
    if row.get("allows_pets") and query_tokens & {"pet", "pets", "thú", "cưng"}:
        reasons.append("Cho phép thú cưng")

    # Khử trùng lặp (không phân biệt hoa/thường), giữ nguyên thứ tự.
    unique = []
    seen_final = set()
    for r in reasons:
        key = r.lower().strip()
        if key and key not in seen_final:
            unique.append(r)
            seen_final.add(key)

    return unique[:max_reasons]


def build_corpus(df):
    """Gộp các trường mô tả của mỗi phòng thành một 'văn bản' để vector hóa."""
    def _row_to_document(row):
        capacity = row.get("capacity") or 0
        pets_text = "cho phép thú cưng pet" if row.get("allows_pets") else ""
        parts = [
            str(row.get("accommodation_name") or ""),
            str(row.get("accommodation_type") or ""),
            str(row.get("city") or ""),
            str(row.get("district") or ""),
            str(row.get("accommodation_description") or ""),
            _parse_json_list(row.get("accommodation_features")),
            str(row.get("room_name") or ""),
            str(row.get("bed_info") or ""),
            str(row.get("area") or ""),
            str(row.get("room_description") or ""),
            _parse_json_list(row.get("room_features")),
            _parse_json_list(row.get("room_services")),
            # Diễn giải sức chứa thành chữ để khớp truy vấn kiểu "cho 2 người"
            f"{capacity} người khách sức chứa {capacity} khách",
            pets_text,
        ]
        return " ".join(p for p in parts if p).lower()

    return df.apply(_row_to_document, axis=1)


def smart_match(query, top_n=3, db_path=None):
    """Trả về top N phòng phù hợp nhất với chuỗi truy vấn tự nhiên.

    Returns: list[dict] gồm room_id, room_name, accommodation_name, city,
    base_price, capacity, score (0..1). Sắp xếp giảm dần theo score.
    """
    if not query or not query.strip():
        return []

    df = load_rooms_dataframe(db_path)
    if df.empty:
        return []

    corpus = build_corpus(df).tolist()

    # Vector hóa cả corpus lẫn truy vấn trong cùng một không gian đặc trưng.
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=1)
    tfidf_matrix = vectorizer.fit_transform(corpus)
    query_vector = vectorizer.transform([query.lower()])

    similarity = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Điểm đánh giá (0..5) chuẩn hóa về 0..1.
    ratings = df["avg_rating"].fillna(0).to_numpy(dtype=float)
    rating_norm = ratings / 5.0

    # Điểm cuối = trọng số tương đồng ngữ nghĩa + trọng số đánh giá.
    # Chỉ cộng điểm rating cho phòng thực sự khớp truy vấn (similarity > 0),
    # tránh gợi ý phòng không liên quan chỉ vì rating cao.
    final_scores = np.where(
        similarity > 0,
        _WEIGHT_SIMILARITY * similarity + _WEIGHT_RATING * rating_norm,
        0.0,
    )

    top_indices = final_scores.argsort()[::-1][:top_n]

    results = []
    for idx in top_indices:
        if final_scores[idx] <= 0:
            continue
        row = df.iloc[idx]
        results.append(
            {
                "room_id": int(row["room_id"]),
                "room_name": row["room_name"],
                "accommodation_name": row["accommodation_name"],
                "city": row["city"],
                "base_price": int(row["base_price"] or 0),
                "capacity": int(row["capacity"] or 0),
                "rating": round(float(ratings[idx]), 1),
                "score": round(float(final_scores[idx]), 4),
                "reasons": _build_reasons(row, query),
            }
        )
    return results


if __name__ == "__main__":
    import sys

    # Bảo đảm in được tiếng Việt trên console Windows (cp1252).
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    user_query = sys.argv[1] if len(sys.argv) > 1 else "phòng cho 2 người có hồ bơi"
    print(f"Truy vấn: {user_query}\n")
    for rank, item in enumerate(smart_match(user_query), start=1):
        reasons = " · ".join(item["reasons"]) if item["reasons"] else "—"
        print(
            f"{rank}. [{item['score']}] {item['room_name']} "
            f"— {item['accommodation_name']} ({item['city']}) "
            f"| {item['base_price']:,}đ | {item['capacity']} khách "
            f"| ⭐ {item['rating']}\n     Lý do: {reasons}"
        )
