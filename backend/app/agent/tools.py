"""
backend/app/agent/tools.py

Tập hợp các công cụ (tools) dùng cho AI Agent SmartBus.
Bao gồm:
  - Tìm kiếm vé xe nội bộ (mock DB)
  - Tìm kiếm thực tế qua Tavily (giá vé, nhà xe, chuyến đi)
  - Trích xuất thông tin vé từ kết quả Tavily bằng Gemini
  - Phát hiện nhập nhằng điểm đón
  - Tạo link Google Maps & booking
"""
from __future__ import annotations

import os
from urllib.parse import quote_plus

import requests

from backend.app.agent.normalization import normalize_city, normalize_text
from backend.app.data.mock_tickets import MOCK_TICKETS
from backend.app.schemas import MockTicket, TripQuery


# ---------------------------------------------------------------------------
# Core helper tools (used internally & by ranking.py)
# ---------------------------------------------------------------------------

def extract_trip_intent(query: TripQuery) -> TripQuery:
    return query


def detect_pickup_ambiguity(pickup_text: str) -> bool:
    """Return True nếu pickup_text có thể bị nhập nhằng (Thanh Phong)."""
    normalized = normalize_text(pickup_text)
    if "thanh phong" not in normalized:
        return False

    place_markers = ("giao xu", "phu my", "vung tau", "diem don", "don tai")
    operator_markers = ("nha xe", "hang xe")
    return any(marker in normalized for marker in place_markers) or not any(
        marker in normalized for marker in operator_markers
    )


def search_mock_tickets(query: TripQuery) -> list[MockTicket]:
    from_city = normalize_city(query.from_city)
    to_city = normalize_city(query.to_city)

    return [
        ticket
        for ticket in MOCK_TICKETS
        if normalize_city(ticket.from_city) == from_city
        and normalize_city(ticket.to_city) == to_city
        and ticket.date == query.date
    ]


def filter_by_operator(tickets: list[MockTicket], operator_text: str) -> list[MockTicket]:
    operator = normalize_text(operator_text)
    return [ticket for ticket in tickets if operator in normalize_text(ticket.operator)]


def suggest_nearby_dates(query: TripQuery) -> list[str]:
    from_city = normalize_city(query.from_city)
    to_city = normalize_city(query.to_city)
    dates = {
        ticket.date
        for ticket in MOCK_TICKETS
        if normalize_city(ticket.from_city) == from_city
        and normalize_city(ticket.to_city) == to_city
    }
    return sorted(dates)[:3]


def build_maps_link(address: str) -> str:
    """Tạo Google Maps search URL cho một địa chỉ."""
    return f"https://www.google.com/maps/search/?api=1&query={quote_plus(address)}"


def build_booking_deeplink(provider: str, ticket_id: str) -> str:
    """Tạo deep-link đặt vé theo nhà cung cấp và mã vé."""
    provider_slug = normalize_text(provider).replace(" ", "-")
    return f"https://smartbus.local/book/{provider_slug}/{ticket_id}"


# ---------------------------------------------------------------------------
# Tavily search tool
# ---------------------------------------------------------------------------

def _call_tavily(query: str, max_results: int = 5) -> list[dict]:
    """
    Gọi Tavily Search API và trả về danh sách kết quả raw.
    Mỗi result có các trường: title, url, content (snippet).
    """
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        return []

    try:
        resp = requests.post(
            "https://api.tavily.com/search",
            json={
                "api_key": api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
                "include_answer": False,
                "include_raw_content": False,
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json().get("results", [])
    except Exception as exc:
        print(f"[Tavily] Error: {exc}")
        return []


def _extract_ticket_info_with_llm(raw_results: list[dict], query_context: str) -> str:
    """
    Dùng Gemini để trích xuất thông tin vé (tên nhà xe, giá vé, giờ đi) từ
    các đoạn text thô của Tavily. Fallback sang tóm tắt đơn giản nếu không có API key.
    """
    if not raw_results:
        return "Không tìm thấy thông tin trên web."

    # Build raw text từ Tavily snippets
    snippets = "\n\n".join(
        f"[{i+1}] {r.get('title', '')}\nURL: {r.get('url', '')}\n{r.get('content', '')}"
        for i, r in enumerate(raw_results)
    )

    gemini_key = os.getenv("GEMINI_API_KEY")
    if not gemini_key:
        # Fallback: trả về tóm tắt thô
        lines = [f"- {r.get('title', 'N/A')}: {r.get('url', '')}" for r in raw_results]
        return "Kết quả tìm kiếm web:\n" + "\n".join(lines)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=gemini_key)
        prompt = (
            f"Bối cảnh truy vấn: {query_context}\n\n"
            "Dưới đây là các đoạn văn bản thu thập từ web. "
            "Hãy trích xuất và trình bày ngắn gọn theo định dạng danh sách: "
            "**Nhà xe** | **Giá vé** | **Giờ khởi hành** | **Điểm đón** | **Link đặt vé**. "
            "Chỉ lấy thông tin thực sự có trong văn bản, bỏ qua những gì không liên quan. "
            "Nếu không tìm thấy thông tin vé xe nào, nói rõ điều đó.\n\n"
            f"Văn bản:\n{snippets}"
        )

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.1,
            ),
        )
        return response.text or "Không trích xuất được thông tin."
    except Exception as exc:
        print(f"[LLM Extract] Error: {exc}")
        lines = [f"- {r.get('title', 'N/A')}: {r.get('url', '')}" for r in raw_results]
        return "Kết quả tìm kiếm web:\n" + "\n".join(lines)


# ---------------------------------------------------------------------------
# Public tools exposed to the Gemini Agent
# ---------------------------------------------------------------------------

def search_by_date_tool(from_city: str, to_city: str, date: str) -> str:
    """
    Tìm kiếm giá vé xe, tên nhà xe và chuyến đi trên web (Tavily) theo tuyến đường và ngày.
    Kết quả được LLM trích xuất thành danh sách gọn.

    Args:
        from_city: Thành phố khởi hành (ví dụ: 'Hà Nội', 'TP.HCM').
        to_city:   Thành phố điểm đến (ví dụ: 'Đà Nẵng', 'Nha Trang').
        date:      Ngày đi theo định dạng YYYY-MM-DD (ví dụ: '2026-06-10').
    """
    query = f"vé xe khách {from_city} đi {to_city} ngày {date} giá vé nhà xe"
    query_context = f"Tìm vé xe từ {from_city} đến {to_city} ngày {date}"

    raw = _call_tavily(query, max_results=5)
    return _extract_ticket_info_with_llm(raw, query_context)


def search_and_format_tickets(
    from_city: str,
    to_city: str,
    date: str,
    priority: str = "price",
    user_lat: float = 21.0369,
    user_lng: float = 105.7897,
) -> str:
    """
    Tìm kiếm và xếp hạng vé xe khách từ cơ sở dữ liệu nội bộ.
    Các thành phố hợp lệ: 'Ha Noi', 'Da Nang', 'Hue', 'Nha Trang', 'Ho Chi Minh'.
    Định dạng ngày: YYYY-MM-DD (ví dụ: 2026-06-06).
    Thứ tự ưu tiên: 'price' (giá rẻ nhất), 'time' (khởi hành sớm nhất),
    hoặc 'pickup_distance' (điểm đón gần nhất).
    """
    from backend.app.schemas import Priority, TripQuery, UserLocation
    from backend.app.agent.service import search_trip

    p = Priority.price
    if priority == "time":
        p = Priority.time
    elif priority == "pickup_distance":
        p = Priority.pickup_distance

    query = TripQuery(
        from_city=from_city,
        to_city=to_city,
        date=date,
        priority=p,
        user_location=UserLocation(label="User location", lat=user_lat, lng=user_lng),
    )

    response = search_trip(query, skip_ambiguity=True)

    if response.path == "failure":
        dates_str = ", ".join(response.suggested_dates) if response.suggested_dates else "không có"
        return (
            f"Không tìm thấy vé xe cho chặng {from_city} → {to_city} ngày {date}.\n"
            f"Các ngày gần nhất có vé: {dates_str}."
        )

    result = (
        f"Đã tìm thấy {len(response.tickets)} vé phù hợp nhất "
        f"({from_city} → {to_city}, {date}, ưu tiên: {p.value}):\n\n"
    )
    for idx, t in enumerate(response.tickets, 1):
        result += (
            f"{idx}. **{t.operator}** (qua {t.provider})\n"
            f"   💰 Giá: {t.price_vnd:,} VNĐ\n"
            f"   🕐 {t.departure_time} → {t.arrival_time}\n"
            f"   📍 Điểm đón: {t.pickup_point} ({t.pickup_distance_km:.1f} km từ bạn)\n"
            f"   🗺️ [Bản đồ]({t.maps_url})  |  🎫 [Đặt vé]({t.booking_url})\n"
            f"   ℹ️ {t.rank_reason}\n\n"
        )

    if response.warning:
        result += f"⚠️ {response.warning}\n"

    return result


def resolve_pickup_ambiguity_tool(pickup_text: str) -> str:
    """
    Kiểm tra nhập nhằng điểm đón. 'Thanh Phong' có thể là:
    1. Địa danh: Giáo xứ Thanh Phong (Phú Mỹ, Vũng Tàu).
    2. Nhà xe: Nhà xe Thanh Phong (tuyến TP.HCM – Đà Nẵng).
    """
    if detect_pickup_ambiguity(pickup_text):
        return (
            "PHÁT HIỆN NHẬP NHẰNG – 'Thanh Phong' có thể hiểu theo 2 nghĩa:\n"
            "1. 📍 Địa danh điểm đón: Giáo xứ Thanh Phong, Phú Mỹ, Vũng Tàu.\n"
            "2. 🚌 Hãng xe: Nhà xe Thanh Phong (tuyến TP.HCM – Đà Nẵng).\n"
            "Vui lòng xác nhận: bạn muốn được đón tại Giáo xứ Thanh Phong, "
            "hay muốn đặt vé Nhà xe Thanh Phong?"
        )
    return "Không phát hiện nhập nhằng điểm đón."
