from enum import Enum

from pydantic import BaseModel, ConfigDict, Field


class Priority(str, Enum):
    price = "price"
    time = "time"
    pickup_distance = "pickup_distance"


class TransportMode(str, Enum):
    all = "all"
    bus = "bus"
    train = "train"
    flight = "flight"


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
    duration_days: int = Field(default=3, ge=1, le=30)
    budget_vnd: int = Field(default=5_000_000, ge=0)
    travelers: int = Field(default=2, ge=1, le=20)
    pickup_text: str = Field(default="")
    user_location: UserLocation = Field(default_factory=UserLocation)
    priority: Priority = Priority.price
    transport_mode: TransportMode = TransportMode.bus


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


class CollectedTransportation(BaseModel):
    transport_type: str
    provider: str
    price: int
    departure: str
    arrival: str
    pickup: str
    source: str = "Internal data"


class CollectedHotel(BaseModel):
    hotel_name: str
    price_per_night: int
    rating: float
    distance_to_center: float


class FoodEstimate(BaseModel):
    category: str
    cost_per_day: int


class RankedPlanOption(BaseModel):
    option: str
    total_cost: int
    comfort_score: int
    speed_score: int
    budget_fit: int
    decision_reason: str


class ItineraryDay(BaseModel):
    day: int
    title: str
    activities: list[str]
    estimated_cost: int


class AgentResponse(BaseModel):
    path: PathType
    summary: str
    tickets: list[TicketOption] = Field(default_factory=list)
    web_results: list[WebSearchResult] = Field(default_factory=list)
    transportation_data: list[CollectedTransportation] = Field(default_factory=list)
    hotels_data: list[CollectedHotel] = Field(default_factory=list)
    food_estimates: list[FoodEstimate] = Field(default_factory=list)
    ranked_plan_options: list[RankedPlanOption] = Field(default_factory=list)
    decision: str | None = None
    itinerary: list[ItineraryDay] = Field(default_factory=list)
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
