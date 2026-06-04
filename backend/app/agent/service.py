from __future__ import annotations

import logging
import time

from backend.app.agent.ranking import rank_tickets
from backend.app.agent.tools import (
    detect_pickup_ambiguity,
    extract_trip_intent,
    filter_by_operator,
    search_mock_tickets,
    search_web_ticket_sources,
    suggest_nearby_dates,
    search_and_format_tickets,
    resolve_pickup_ambiguity_tool,
    search_by_date_tool,
    search_stay_options_tool,
    search_travel_guide_tool,
)
import os
import re
from typing import Any

from backend.app.agent.normalization import normalize_text
from backend.app.observability import elapsed_ms, log_json, summarize_text
from backend.app.schemas import (
    AgentResponse,
    ClarificationChoice,
    ClarificationRequest,
    PathType,
    TripQuery,
    ChatRequest,
)

logger = logging.getLogger("smarttravel.agent")


CHAT_CITY_ALIASES = {
    "hn": "Ha Noi",
    "ha noi": "Ha Noi",
    "hanoi": "Ha Noi",
    "hai phong": "Hai Phong",
    "cao bang": "Cao Bang",
    "thanh hoa": "Thanh Hoa",
    "da nang": "Da Nang",
    "danang": "Da Nang",
    "dn": "Da Nang",
    "hue": "Hue",
    "nha trang": "Nha Trang",
    "ho chi minh": "Ho Chi Minh",
    "sai gon": "Ho Chi Minh",
    "saigon": "Ho Chi Minh",
    "hcm": "Ho Chi Minh",
    "tp hcm": "Ho Chi Minh",
}


def search_trip(query: TripQuery, *, skip_ambiguity: bool = False) -> AgentResponse:
    start = time.perf_counter()
    log_json(
        logger,
        logging.INFO,
        "search.stage.intent_extract.start",
        stage="thinking",
        query=query.model_dump(),
        skip_ambiguity=skip_ambiguity,
    )
    intent = extract_trip_intent(query)
    log_json(
        logger,
        logging.INFO,
        "search.stage.intent_extract.done",
        stage="thinking",
        intent=intent.model_dump(),
    )

    if intent.pickup_text and not skip_ambiguity and detect_pickup_ambiguity(intent.pickup_text):
        response = AgentResponse(
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
        log_json(
            logger,
            logging.INFO,
            "search.response",
            stage="thinking",
            path=response.path.value,
            ticket_count=len(response.tickets),
            elapsed_ms=elapsed_ms(start),
        )
        return response

    tickets = search_mock_tickets(intent)
    if not tickets:
        suggested_dates = suggest_nearby_dates(intent)
        web_results = search_web_ticket_sources(intent)
        if web_results:
            response = AgentResponse(
                path=PathType.low_confidence,
                summary="Tìm thấy nguồn tham khảo từ web cho tuyến này.",
                warning=None,
                web_results=web_results,
                suggested_dates=suggested_dates,
            )
            log_json(
                logger,
                logging.INFO,
                "search.response",
                stage="thinking",
                path=response.path.value,
                ticket_count=0,
                web_result_count=len(web_results),
                suggested_dates=suggested_dates,
                elapsed_ms=elapsed_ms(start),
            )
            return response

        response = AgentResponse(
            path=PathType.failure,
            summary="Không tìm thấy vé phù hợp cho ngày đã chọn.",
            warning=(
                "Không tìm thấy dữ liệu nội bộ hoặc nguồn web từ Tavily. "
                "Thử đổi ngày đi hoặc kiểm tra lại tên tuyến."
            ),
            suggested_dates=suggested_dates,
        )
        log_json(
            logger,
            logging.INFO,
            "search.response",
            stage="thinking",
            path=response.path.value,
            ticket_count=0,
            suggested_dates=suggested_dates,
            elapsed_ms=elapsed_ms(start),
        )
        return response

    ranked = rank_tickets(tickets, intent.priority)
    warning = _build_low_confidence_warning(ranked)

    response = AgentResponse(
        path=PathType.low_confidence if warning else PathType.happy,
        summary=f"Đã tìm thấy {len(ranked)} lựa chọn phù hợp nhất theo ưu tiên {intent.priority.value}.",
        tickets=ranked,
        warning=warning,
    )
    log_json(
        logger,
        logging.INFO,
        "search.response",
        stage="thinking",
        path=response.path.value,
        ticket_count=len(response.tickets),
        top_ticket_id=response.tickets[0].id if response.tickets else None,
        elapsed_ms=elapsed_ms(start),
    )
    return response


def clarify_trip(request: ClarificationRequest) -> AgentResponse:
    log_json(
        logger,
        logging.INFO,
        "clarify.request",
        stage="thinking",
        choice=request.choice.value,
        query=request.query.model_dump(),
    )
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


def _function_call_args(args: Any) -> dict:
    if args is None:
        return {}
    if isinstance(args, dict):
        return dict(args)
    try:
        return dict(args)
    except Exception:
        return {}


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


def _parse_date_from_message(normalized: str) -> str:
    date_match = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", normalized)
    if date_match:
        return f"{date_match.group(1)}-{int(date_match.group(2)):02d}-{int(date_match.group(3)):02d}"

    date_match_viet = re.search(r"(\d{1,2})[-/](\d{1,2})[-/](\d{4})", normalized)
    if date_match_viet:
        return f"{date_match_viet.group(3)}-{int(date_match_viet.group(2)):02d}-{int(date_match_viet.group(1)):02d}"

    date_match_short = re.search(r"(ngay\s+)?(\d{1,2})[/-](\d{1,2})", normalized)
    if date_match_short:
        d = int(date_match_short.group(2))
        m = int(date_match_short.group(3))
        return f"2026-{m:02d}-{d:02d}"

    return "2026-06-06"


def _parse_priority_from_message(normalized: str) -> str:
    if "re" in normalized or "gia" in normalized or "thap" in normalized:
        return "price"
    if "som" in normalized or "gio" in normalized or "thoi gian" in normalized:
        return "time"
    if "gan" in normalized or "don" in normalized or "khoang cach" in normalized:
        return "pickup_distance"
    return "price"


def _parse_route_from_message(message: str) -> tuple[str, str, str, str] | None:
    normalized = normalize_text(message)
    if not any(keyword in normalized for keyword in ("tim", "ve", "xe", "di", "den", "toi")):
        return None

    matches: list[tuple[int, int, str]] = []
    for alias, city in sorted(CHAT_CITY_ALIASES.items(), key=lambda item: len(item[0]), reverse=True):
        pattern = rf"(?<!\w){re.escape(alias)}(?!\w)"
        for match in re.finditer(pattern, normalized):
            matches.append((match.start(), match.end(), city))

    matches.sort(key=lambda item: (item[0], -(item[1] - item[0])))
    ordered_cities: list[str] = []
    occupied_until = -1
    for start, end, city in matches:
        if start < occupied_until:
            continue
        occupied_until = end
        if city not in ordered_cities:
            ordered_cities.append(city)

    if len(ordered_cities) < 2:
        return None

    from_city, to_city = ordered_cities[0], ordered_cities[1]
    return (
        from_city,
        to_city,
        _parse_date_from_message(normalized),
        _parse_priority_from_message(normalized),
    )


def mock_chat_agent(message: str, history: list) -> str:
    normalized = message.lower()

    if "thanh phong" in normalized:
        return (
            "Bạn muốn được đón tại địa danh Giáo xứ Thanh Phong (Phú Mỹ, Vũng Tàu), "
            "hay muốn tìm Nhà xe Thanh Phong?"
        )

    parsed_route = _parse_route_from_message(message)
    if parsed_route:
        from_city, to_city, date, priority = parsed_route
        from backend.app.agent.tools import search_and_format_tickets
        return search_and_format_tickets(from_city, to_city, date, priority)

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
        return "Giá vé thay đổi theo phương tiện, tuyến và thời điểm. Bạn có thể tìm tuyến cụ thể để SmartTravel gợi ý vé xe, tàu hoặc máy bay từ dữ liệu nội bộ và nguồn web."
    if "giờ" in normalized or "sớm" in normalized or "muộn" in normalized:
        return "Bạn muốn đi sớm hay tối? Chọn ưu tiên 'Giờ đi' để SmartTravel gợi ý phương án khởi hành phù hợp."
    if "đón" in normalized or "pickup" in normalized:
        return "Nhập điểm đón, nhà ga, sân bay hoặc ghi chú vị trí để SmartTravel ưu tiên phương án thuận tiện hơn."
    if any(word in normalized for word in ("khách sạn", "khach san", "đặt phòng", "dat phong", "homestay", "lưu trú", "luu tru")):
        return search_stay_options_tool(message)
    if any(word in normalized for word in ("lịch trình", "lich trinh", "đi đâu", "di dau", "chơi", "choi", "du lịch", "du lich")):
        return search_travel_guide_tool(message)
    if "đặt" in normalized or "book" in normalized or "mua" in normalized:
        return "Sau khi tìm được phương án phù hợp, mở nguồn hoặc bấm 'Đặt / kiểm tra' để sang trang nhà cung cấp. Tôi cũng có thể gợi ý khu vực lưu trú và nguồn đặt phòng."

    return "Tôi hiểu câu hỏi của bạn. Hãy hỏi tôi tìm vé xe/tàu/máy bay, gợi ý lịch trình, địa điểm du lịch, trải nghiệm nên thử hoặc khu vực đặt phòng."


def chat_agent(request: ChatRequest) -> str:
    start = time.perf_counter()
    log_json(
        logger,
        logging.INFO,
        "chat.request",
        stage="thinking",
        message=summarize_text(request.message),
        history_count=len(request.history),
        gemini_configured=bool(os.getenv("GEMINI_API_KEY")),
        tavily_configured=bool(os.getenv("TAVILY_API_KEY")),
    )

    parsed_route = _parse_route_from_message(request.message)
    if parsed_route and "thanh phong" not in normalize_text(request.message):
        from_city, to_city, date, priority = parsed_route
        log_json(
            logger,
            logging.INFO,
            "chat.route_detected",
            stage="thinking",
            from_city=from_city,
            to_city=to_city,
            date=date,
            priority=priority,
        )
        return search_and_format_tickets(from_city, to_city, date, priority)

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        log_json(
            logger,
            logging.WARNING,
            "chat.fallback",
            stage="thinking",
            reason="missing_GEMINI_API_KEY",
        )
        return mock_chat_agent(request.message, request.history)

    try:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=api_key)
        log_json(
            logger,
            logging.INFO,
            "chat.stage.build_contents",
            stage="thinking",
            history_count=len(request.history),
        )

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
            "Bạn là Trợ lý SmartTravel, AI hỗ trợ lập kế hoạch du lịch tại Việt Nam.\n"
            "NGUYÊN TẮC SỬ DỤNG TOOLS:\n"
            "1. Khi khách hỏi tìm vé với TUYẾN CỤ THỂ (có từ/đến), gọi `search_and_format_tickets` "
            "để tìm trong database nội bộ trước. Database hiện có dữ liệu mẫu cho một số tuyến xe.\n"
            "2. Nếu không có dữ liệu nội bộ, hoặc khách hỏi giá vé/giờ đi thực tế cho vé xe, tàu, máy bay, "
            "gọi `search_by_date_tool` để tìm qua web (Tavily) rồi trả kết quả đã được trích xuất.\n"
            "3. Khi khách nhắc tới điểm đón 'Thanh Phong', luôn gọi `resolve_pickup_ambiguity_tool` "
            "và hỏi rõ trước khi tìm vé.\n"
            "4. Khi khách hỏi lịch trình, tiện ích, địa điểm du lịch, nên đi như thế nào, trải nghiệm, ăn uống, "
            "hoặc khu vực đặt phòng, gọi `search_travel_guide_tool` để lấy nguồn web trước khi gợi ý.\n"
            "5. Khi khách hỏi riêng về khách sạn, homestay hoặc đặt phòng, gọi `search_stay_options_tool`.\n"
            "6. Không bao giờ bịa giá vé, giờ đi, tình trạng phòng hoặc còn chỗ. Nêu rõ cần mở nguồn nhà cung cấp để xác nhận.\n"
            "7. Trả lời ngắn gọn, lịch sự, hoàn toàn bằng tiếng Việt."
        )

        # Tool registry: maps function name -> callable
        tool_registry = {
            "search_and_format_tickets": search_and_format_tickets,
            "search_by_date_tool": search_by_date_tool,
            "resolve_pickup_ambiguity_tool": resolve_pickup_ambiguity_tool,
            "search_travel_guide_tool": search_travel_guide_tool,
            "search_stay_options_tool": search_stay_options_tool,
        }

        # First LLM call
        llm_start = time.perf_counter()
        log_json(
            logger,
            logging.INFO,
            "llm.chat.request",
            stage="llm",
            model="gemini-2.5-flash",
            turn="initial",
            tools=list(tool_registry.keys()),
        )
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=system_instruction,
                tools=list(tool_registry.values()),
                automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
            )
        )
        log_json(
            logger,
            logging.INFO,
            "llm.chat.response",
            stage="llm",
            turn="initial",
            elapsed_ms=elapsed_ms(llm_start),
            tool_calls=[fc.name for fc in (response.function_calls or [])],
            text_preview=summarize_text(response.text or ""),
        )

        # ReAct loop: execute tool calls and feed results back
        MAX_TURNS = 3
        for turn in range(1, MAX_TURNS + 1):
            if not response.function_calls:
                break

            # Append the model's tool-call turn
            contents.append(response.candidates[0].content)

            # Execute ALL requested tool calls this turn
            tool_response_parts = []
            for fc in response.function_calls:
                fn = tool_registry.get(fc.name)
                args = _function_call_args(fc.args)
                tool_start = time.perf_counter()
                log_json(
                    logger,
                    logging.INFO,
                    "llm.tool_call",
                    stage="tool",
                    turn=turn,
                    tool=fc.name,
                    args=args,
                )
                if fn is None:
                    result = f"Error: tool '{fc.name}' không tồn tại."
                else:
                    try:
                        result = fn(**args)
                    except Exception as tool_err:
                        result = f"Lỗi khi gọi tool '{fc.name}': {tool_err}"
                        log_json(
                            logger,
                            logging.ERROR,
                            "llm.tool_error",
                            stage="tool",
                            turn=turn,
                            tool=fc.name,
                            error=str(tool_err),
                            elapsed_ms=elapsed_ms(tool_start),
                        )

                log_json(
                    logger,
                    logging.INFO,
                    "llm.tool_response",
                    stage="tool",
                    turn=turn,
                    tool=fc.name,
                    elapsed_ms=elapsed_ms(tool_start),
                    result_preview=summarize_text(result),
                )

                tool_response_parts.append(
                    types.Part.from_function_response(
                        name=fc.name,
                        response={"result": result},
                    )
                )

            contents.append(
                types.Content(role="user", parts=tool_response_parts)
            )

            # Next LLM turn to synthesise tool results
            llm_start = time.perf_counter()
            log_json(
                logger,
                logging.INFO,
                "llm.chat.request",
                stage="llm",
                model="gemini-2.5-flash",
                turn=f"after_tool_{turn}",
            )
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    tools=list(tool_registry.values()),
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
                )
            )
            log_json(
                logger,
                logging.INFO,
                "llm.chat.response",
                stage="llm",
                turn=f"after_tool_{turn}",
                elapsed_ms=elapsed_ms(llm_start),
                tool_calls=[fc.name for fc in (response.function_calls or [])],
                text_preview=summarize_text(response.text or ""),
            )

        final_text = response.text or "Tôi không nhận được phản hồi."
        log_json(
            logger,
            logging.INFO,
            "chat.response",
            stage="thinking",
            elapsed_ms=elapsed_ms(start),
            reply_preview=summarize_text(final_text),
        )
        return final_text

    except Exception as e:
        log_json(
            logger,
            logging.ERROR,
            "chat.error",
            stage="thinking",
            error=str(e),
            elapsed_ms=elapsed_ms(start),
        )
        return mock_chat_agent(request.message, request.history)
