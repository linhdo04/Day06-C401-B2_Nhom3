from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.agent.service import clarify_trip, search_trip
from backend.app.schemas import AgentResponse, ClarificationRequest, HealthResponse, TripQuery

app = FastAPI(
    title="SmartBus AI",
    description="Python backend for the SmartBus AI Day 06 prototype.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/search", response_model=AgentResponse)
def search(query: TripQuery) -> AgentResponse:
    return search_trip(query)


@app.post("/api/clarify", response_model=AgentResponse)
def clarify(request: ClarificationRequest) -> AgentResponse:
    return clarify_trip(request)
