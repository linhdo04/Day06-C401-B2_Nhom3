from __future__ import annotations

from backend.app.agent.ranking import rank_tickets
from backend.app.agent.tools import (
    detect_pickup_ambiguity,
    extract_trip_intent,
    filter_by_operator,
    search_mock_tickets,
    suggest_nearby_dates,
    search_and_format_tickets,
    resolve_pickup_ambiguity_tool,
    search_by_date_tool,
)
import os
import re
from backend.app.schemas import (
    AgentResponse,
    ClarificationChoice,
    ClarificationRequest,
    PathType,
    TripQuery,
    ChatRequest,
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


def mock_chat_agent(message: str, history: list) -> str:
    normalized = message.lower()

    if "thanh phong" in normalized:
        return (
            "Bạn muốn được đón tại địa danh Giáo xứ Thanh Phong (Phú Mỹ, Vũng Tàu), "
            "hay muốn tìm Nhà xe Thanh Phong?"
        )

    from_city = None
    to_city = None
    date = "2026-06-06"
    priority = "price"

    if "ha noi" in normalized or "hà nội" in normalized or "hn" in normalized:
        from_city = "Ha Noi"
    if "da nang" in normalized or "đà nẵng" in normalized or "dn" in normalized:
        to_city = "Da Nang"
    if "hue" in normalized or "huế" in normalized:
        to_city = "Hue"
    if "nha trang" in normalized or "nt" in normalized:
        to_city = "Nha Trang"
    if "ho chi minh" in normalized or "sài gòn" in normalized or "hcm" in normalized or "sai gon" in normalized:
        if from_city is None and "từ" in normalized:
            from_city = "Ho Chi Minh"
        else:
            to_city = "Ho Chi Minh"

    date_match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", normalized)
    if date_match:
        date = f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"
    else:
        date_match_viet = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", normalized)
        if date_match_viet:
            date = f"{date_match_viet.group(3)}-{int(date_match_viet.group(2)):02d}-{int(date_match_viet.group(1)):02d}"
        else:
            date_match_short = re.search(r"(ngày\s+)?(\d{1,2})[/-](\d{1,2})", normalized)
            if date_match_short:
                d = int(date_match_short.group(2))
                m = int(date_match_short.group(3))
                date = f"2026-{m:02d}-{d:02d}"

    if "rẻ" in normalized or "giá" in normalized or "thấp" in normalized:
        priority = "price"
    elif "sớm" in normalized or "giờ" in normalized or "thời gian" in normalized:
        priority = "time"
    elif "gần" in normalized or "đón" in normalized or "khoảng cách" in normalized:
        priority = "pickup_distance"

    if from_city and to_city:
        from backend.app.agent.tools import search_and_format_tickets
        return search_and_format_tickets(from_city, to_city, date, priority)

    if "giá" in normalized or "vé" in normalized or "tiền" in normalized:
        return "Giá vé thường dao động từ 150.000 – 500.000 VNĐ tùy tuyến và hãng xe. Bạn có thể chọn ưu tiên 'Giá thấp nhất' để SmartBus xếp hạng theo giá."
    if "giờ" in normalized or "sớm" in normalized or "muộn" in normalized:
        return "Bạn muốn đi sớm hay tối? Chọn ưu tiên 'Giờ đi sớm nhất' và SmartBus sẽ hiển thị các chuyến sớm nhất trong ngày."
    if "đón" in normalized or "pickup" in normalized:
        return "Nhập địa điểm đón của bạn vào ô 'Điểm đón', SmartBus sẽ tính khoảng cách từ bạn đến từng điểm đón và xếp hạng theo gần nhất."
    if "đặt" in normalized or "book" in normalized or "mua" in normalized:
        return "Sau khi tìm được vé phù hợp, bấm 'Đặt vé' trên thẻ kết quả để chuyển đến trang đặt vé của nhà cung cấp."

    return "Tôi hiểu câu hỏi của bạn. Hãy thử tìm kiếm bằng cách hỏi tôi tìm vé (ví dụ: 'tìm vé từ Hà Nội đi Đà Nẵng ngày 6/6') hoặc hỏi về điểm đón, giá vé!"


def chat_agent(request: ChatRequest) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return mock_chat_agent(request.message, request.history)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)

        # Build conversation contents from history
        contents = []
        for msg in request.history:
            role = "user" if msg.role == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=msg.text)]
                )
            )

        # Append current message if not already last in history
        if not request.history or request.history[-1].text != request.message:
            contents.append(
                types.Content(
                    role="user",
                    parts=[types.Part.from_text(text=request.message)]
                )
            )

        system_instruction = (
            "Bạn là Trợ lý SmartBus, AI chuyên hỗ trợ tìm vé xe khách liên tỉnh Việt Nam.\n"
            "NGUYÊN TẮC SỬ DỤNG TOOLS:\n"
            "1. Khi khách hỏi tìm vé với TUYẾN CỤ THỂ (có từ/đến), gọi `search_and_format_tickets` "
            "để tìm trong database nội bộ trước.\n"
            "2. Nếu không có vé trong database, hoặc khách hỏi về GIÁ VÉ / NHÀ XE THỰC TẾ trên mạng, "
            "gọi `search_by_date_tool` để tìm qua web (Tavily) rồi trả kết quả đã được trích xuất.\n"
            "3. Khi khách nhắc tới điểm đón 'Thanh Phong', luôn gọi `resolve_pickup_ambiguity_tool` "
            "và hỏi rõ trước khi tìm vé.\n"
            "4. Không bao giờ bịa thông tin giá vé hoặc nhà xe. Chỉ dùng kết quả từ tools.\n"
            "5. Trả lời ngắn gọn, lịch sự, hoàn toàn bằng tiếng Việt."
        )

        # Tool registry: maps function name -> callable
        tool_registry = {
            "search_and_format_tickets": search_and_format_tickets,
            "search_by_date_tool": search_by_date_tool,
            "resolve_pickup_ambiguity_tool": resolve_pickup_ambiguity_tool,
        }

        # First LLM call
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=list(tool_registry.values()),
            )
        )

        # ReAct loop: execute tool calls and feed results back
        MAX_TURNS = 3
        for _ in range(MAX_TURNS):
            if not response.function_calls:
                break

            # Append the model's tool-call turn
            contents.append(response.candidates[0].content)

            # Execute ALL requested tool calls this turn
            tool_response_parts = []
            for fc in response.function_calls:
                fn = tool_registry.get(fc.name)
                if fn is None:
                    result = f"Error: tool '{fc.name}' không tồn tại."
                else:
                    try:
                        result = fn(**fc.args)
                    except Exception as tool_err:
                        result = f"Lỗi khi gọi tool '{fc.name}': {tool_err}"

                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            contents.append(
                types.Content(role="tool", parts=tool_response_parts)
            )

            # Next LLM turn to synthesise tool results
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                )
            )

        return response.text or "Tôi không nhận được phản hồi."

    except Exception as e:
        print(f"[chat_agent] Gemini error: {e}")
        return mock_chat_agent(request.message, request.history)

