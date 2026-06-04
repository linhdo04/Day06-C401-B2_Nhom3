from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    price = "price"
    time = "time"
    pickup_distance = "pickup_distance"


class PathType(str, Enum):
    happy = "happy"
    low_confidence = "low_confidence"
    failure = "failure"
    clarification = "clarification"


class ClarificationChoice(str, Enum):
    pickup_place = "pickup_place"
    bus_operator = "bus_operator"


class UserLocation(BaseModel):
    label: str = "Cau Giay, Hanoi"
    lat: float = 21.0369
    lng: float = 105.7897


class TripQuery(BaseModel):
    from_city: str = Field(default="Ha Noi")
    to_city: str = Field(default="Da Nang")
    date: str = Field(default="2026-06-06")
    pickup_text: str = Field(default="")
    user_location: UserLocation = Field(default_factory=UserLocation)
    priority: Priority = Priority.price


class TicketOption(BaseModel):
    id: str
    provider: str
    operator: str
    from_city: str
    to_city: str
    date: str
    departure_time: str
    arrival_time: str
    price_vnd: int
    pickup_point: str
    pickup_address: str
    pickup_distance_km: float
    booking_url: str
    maps_url: str
    rank_reason: str


class WebSearchResult(BaseModel):
    title: str
    url: str
    snippet: str = ""
    source: str = "Tavily"


class AgentResponse(BaseModel):
    path: PathType
    summary: str
    tickets: list[TicketOption] = Field(default_factory=list)
    web_results: list[WebSearchResult] = Field(default_factory=list)
    warning: str | None = None
    clarification_question: str | None = None
    clarification_options: list[ClarificationChoice] = Field(default_factory=list)
    suggested_dates: list[str] = Field(default_factory=list)


class ClarificationRequest(BaseModel):
    query: TripQuery
    choice: ClarificationChoice


class ChatMessage(BaseModel):
    role: str
    text: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    reply: str


class HealthResponse(BaseModel):
    status: str


class MockTicket(BaseModel):
    model_config = ConfigDict(frozen=True)

    id: str
    provider: str
    operator: str
    from_city: str
    to_city: str
    date: str
    departure_time: str
    arrival_time: str
    price_vnd: int
    pickup_point: str
    pickup_address: str
    pickup_distance_km: float
