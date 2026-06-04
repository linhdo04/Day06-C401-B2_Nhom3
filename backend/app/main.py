from __future__ import annotations

import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request

from backend.app.config import load_environment
from backend.app.agent.service import clarify_trip, search_trip, chat_agent
from backend.app.observability import (
    configure_logging,
    elapsed_ms,
    log_json,
    new_request_id,
    request_id_ctx,
    summarize_text,
)
from backend.app.schemas import (
    AgentResponse,
    ClarificationRequest,
    HealthResponse,
    TripQuery,
    ChatRequest,
    ChatResponse,
)

load_environment()
configure_logging()
logger = logging.getLogger("smarttravel.api")

app = FastAPI(
    title="SmartTravel AI",
    description="Python backend for the SmartTravel AI Day 06 prototype.",
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


@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = request.headers.get("x-request-id") or new_request_id()
    token = request_id_ctx.set(request_id)
    start = time.perf_counter()

    body = await request.body()
    log_json(
        logger,
        logging.INFO,
        "http.request",
        method=request.method,
        path=request.url.path,
        query=str(request.url.query),
        body=summarize_text(body.decode("utf-8", errors="replace")),
    )

    async def receive():
        return {"type": "http.request", "body": body, "more_body": False}

    try:
        response = await call_next(Request(request.scope, receive))
        log_json(
            logger,
            logging.INFO,
            "http.response",
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            elapsed_ms=elapsed_ms(start),
        )
        response.headers["x-request-id"] = request_id
        return response
    except Exception as exc:
        log_json(
            logger,
            logging.ERROR,
            "http.error",
            method=request.method,
            path=request.url.path,
            error=str(exc),
            elapsed_ms=elapsed_ms(start),
        )
        raise
    finally:
        request_id_ctx.reset(token)


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.post("/api/search", response_model=AgentResponse)
def search(query: TripQuery) -> AgentResponse:
    return search_trip(query)


@app.post("/api/clarify", response_model=AgentResponse)
def clarify(request: ClarificationRequest) -> AgentResponse:
    return clarify_trip(request)


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    return ChatResponse(reply=chat_agent(request))
