from backend.app.agent.service import clarify_trip, search_trip
from backend.app.schemas import (
    ClarificationChoice,
    ClarificationRequest,
    PathType,
    Priority,
    TripQuery,
    WebSearchResult,
)


def test_ranks_cheapest_first() -> None:
    response = search_trip(TripQuery(priority=Priority.price))

    assert response.path == PathType.low_confidence
    assert response.tickets[0].operator == "Sao Viet Express"
    assert response.tickets[0].price_vnd == 390000


def test_ranks_nearest_pickup_first() -> None:
    response = search_trip(TripQuery(priority=Priority.pickup_distance))

    assert response.tickets[0].operator == "Queen Cafe VIP"
    assert response.tickets[0].pickup_distance_km == 1.2


def test_finds_hanoi_to_thanh_hoa_with_accented_city_names() -> None:
    response = search_trip(
        TripQuery(
            from_city="Hà Nội",
            to_city="Thanh Hóa",
            date="2026-06-06",
            priority=Priority.price,
        )
    )

    assert response.path == PathType.happy
    assert len(response.tickets) == 3
    assert response.tickets[0].operator == "Thanh Hoa Limousine"
    assert response.tickets[0].price_vnd == 100000


def test_detects_thanh_phong_ambiguity() -> None:
    response = search_trip(TripQuery(pickup_text="Giao xu Thanh Phong"))

    assert response.path == PathType.clarification
    assert response.clarification_options == [
        ClarificationChoice.pickup_place,
        ClarificationChoice.bus_operator,
    ]


def test_suggests_nearby_dates_when_no_ticket(monkeypatch) -> None:
    monkeypatch.setattr("backend.app.agent.service.search_web_ticket_sources", lambda query: [])

    response = search_trip(TripQuery(to_city="Nha Trang", date="2026-06-06"))

    assert response.path == PathType.failure
    assert response.suggested_dates == ["2026-06-07"]


def test_falls_back_to_tavily_sources_when_mock_has_no_ticket(monkeypatch) -> None:
    monkeypatch.setattr(
        "backend.app.agent.service.search_web_ticket_sources",
        lambda query: [
            WebSearchResult(
                title="Vé xe Hà Nội đi Hải Phòng",
                url="https://example.com/ha-noi-hai-phong",
                snippet="Có nhiều nhà xe mở bán theo ngày.",
            )
        ],
    )

    response = search_trip(TripQuery(from_city="Hà Nội", to_city="Hải Phòng"))

    assert response.path == PathType.low_confidence
    assert response.tickets == []
    assert len(response.web_results) == 1
    assert response.web_results[0].url == "https://example.com/ha-noi-hai-phong"


def test_tavily_call_uses_bearer_auth(monkeypatch) -> None:
    from backend.app.agent import tools

    captured: dict = {}

    class FakeResponse:
        status_code = 200

        def raise_for_status(self) -> None:
            return None

        def json(self) -> dict:
            return {"results": [{"title": "Ticket result", "url": "https://example.com"}]}

    def fake_post(url: str, *, headers: dict, json: dict, timeout: int) -> FakeResponse:
        captured["url"] = url
        captured["headers"] = headers
        captured["json"] = json
        captured["timeout"] = timeout
        return FakeResponse()

    monkeypatch.setenv("TAVILY_API_KEY", "tvly-test")
    monkeypatch.setattr(tools.requests, "post", fake_post)

    results = tools._call_tavily("vé xe Hà Nội đi Hải Phòng", max_results=1)

    assert results
    assert captured["headers"]["Authorization"] == "Bearer tvly-test"
    assert "api_key" not in captured["json"]
    assert captured["json"]["country"] == "vietnam"


def test_clarify_pickup_place_returns_ranked_options() -> None:
    query = TripQuery(pickup_text="Giao xu Thanh Phong")
    response = clarify_trip(ClarificationRequest(query=query, choice=ClarificationChoice.pickup_place))

    assert response.path == PathType.low_confidence
    assert response.tickets
    assert "địa danh" in response.warning


def test_chat_agent_detects_ambiguity() -> None:
    from backend.app.agent.service import chat_agent
    from backend.app.schemas import ChatRequest

    req = ChatRequest(message="đón tôi ở Thanh Phong")
    reply = chat_agent(req)
    assert "Giáo xứ Thanh Phong" in reply or "Nhà xe Thanh Phong" in reply
    assert "Bạn muốn" in reply or "nhập nhằng" in reply


def test_chat_agent_finds_tickets() -> None:
    from backend.app.agent.service import chat_agent
    from backend.app.schemas import ChatRequest

    req = ChatRequest(message="tìm vé từ Hà Nội đi Đà Nẵng ngày 6/6/2026")
    reply = chat_agent(req)
    assert "Sao Viet Express" in reply or "Queen Cafe VIP" in reply
    assert "390,000" in reply or "420,000" in reply


def test_chat_agent_searches_route_before_gemini(monkeypatch) -> None:
    from backend.app.agent.service import chat_agent
    from backend.app.schemas import ChatRequest

    monkeypatch.setattr(
        "backend.app.agent.service.search_web_ticket_sources",
        lambda query: [
            WebSearchResult(
                title="Đặt vé xe từ Hà Nội đi Cao Bằng - Vexere.com",
                url="https://vexere.com/vi-VN/ve-xe-khach-tu-ha-noi-di-cao-bang-cao-bang-124t21211.html",
                snippet="Đặt mua vé xe 15 nhà xe đi Cao Bằng từ Hà Nội.",
            )
        ],
    )

    req = ChatRequest(message="tìm cho tôi vé rẻ nhất đi HN đến Cao Bằng ngày 6/6/2026")
    reply = chat_agent(req)

    assert "Hà Nội" in reply or "Ha Noi" in reply
    assert "Cao Bang" in reply
    assert "Vexere.com" in reply
    assert "có muốn tôi tìm" not in reply.lower()
