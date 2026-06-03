from __future__ import annotations

from backend.app.agent.ranking import rank_tickets
from backend.app.agent.tools import (
    detect_pickup_ambiguity,
    extract_trip_intent,
    filter_by_operator,
    search_mock_tickets,
    suggest_nearby_dates,
)
from backend.app.schemas import (
    AgentResponse,
    ClarificationChoice,
    ClarificationRequest,
    PathType,
    TripQuery,
)


def search_trip(query: TripQuery, *, skip_ambiguity: bool = False) -> AgentResponse:
    intent = extract_trip_intent(query)

    if intent.pickup_text and not skip_ambiguity and detect_pickup_ambiguity(intent.pickup_text):
        return AgentResponse(
            path=PathType.clarification,
            summary="Cần xác nhận ý nghĩa của 'Thanh Phong' trước khi gợi ý vé.",
            clarification_question=(
                "Bạn muốn được đón tại địa danh Giáo xứ Thanh Phong, "
                "hay muốn tìm Nhà xe Thanh Phong?"
            ),
            clarification_options=[
                ClarificationChoice.pickup_place,
                ClarificationChoice.bus_operator,
            ],
        )

    tickets = search_mock_tickets(intent)
    if not tickets:
        suggested_dates = suggest_nearby_dates(intent)
        return AgentResponse(
            path=PathType.failure,
            summary="Không tìm thấy vé phù hợp cho ngày đã chọn.",
            warning="Thử đổi ngày đi hoặc nới lỏng điểm đón để xem thêm lựa chọn.",
            suggested_dates=suggested_dates,
        )

    ranked = rank_tickets(tickets, intent.priority)
    warning = _build_low_confidence_warning(ranked)

    return AgentResponse(
        path=PathType.low_confidence if warning else PathType.happy,
        summary=f"Đã tìm thấy {len(ranked)} lựa chọn phù hợp nhất theo ưu tiên {intent.priority.value}.",
        tickets=ranked,
        warning=warning,
    )


def clarify_trip(request: ClarificationRequest) -> AgentResponse:
    if request.choice == ClarificationChoice.pickup_place:
        response = search_trip(request.query, skip_ambiguity=True)
        response.warning = (
            "Đã xử lý Thanh Phong là địa danh điểm đón. Hãy kiểm tra địa chỉ đầy đủ và Maps "
            "trước khi bấm đặt vé."
        )
        response.path = PathType.low_confidence
        return response

    tickets = filter_by_operator(search_mock_tickets(request.query), "Thanh Phong")
    if not tickets:
        return AgentResponse(
            path=PathType.failure,
            summary="Không có Nhà xe Thanh Phong trên chặng/ngày đã chọn.",
            warning="Hãy chọn ý nghĩa là địa danh điểm đón nếu bạn đang nói về Giáo xứ Thanh Phong.",
            suggested_dates=suggest_nearby_dates(request.query),
        )

    return AgentResponse(
        path=PathType.low_confidence,
        summary="Đã lọc theo Nhà xe Thanh Phong.",
        tickets=rank_tickets(tickets, request.query.priority),
        warning="Kết quả đã bị giới hạn theo nhà xe, có thể bỏ lỡ lựa chọn rẻ hơn/gần hơn.",
    )


def _build_low_confidence_warning(tickets: list) -> str | None:
    if len(tickets) == 1:
        ticket = tickets[0]
        return (
            f"Chỉ còn 1 lựa chọn; điểm đón cách bạn {ticket.pickup_distance_km:.1f} km."
        )

    first_ticket = tickets[0]
    if first_ticket.pickup_distance_km > 5:
        return "Lựa chọn đứng đầu có điểm đón xa hơn 5 km; hãy mở Maps để xác nhận trước khi đặt."

    return None
