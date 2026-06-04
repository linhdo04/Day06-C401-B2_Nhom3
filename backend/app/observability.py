from __future__ import annotations

import json
import logging
import os
import time
import uuid
from contextvars import ContextVar
from typing import Any


request_id_ctx: ContextVar[str] = ContextVar("request_id", default="-")


class RequestIdFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        record.request_id = request_id_ctx.get()
        return True


def configure_logging() -> None:
    level = os.getenv("SMARTBUS_LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    handler.addFilter(RequestIdFilter())
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s %(levelname)s [%(request_id)s] %(name)s - %(message)s"
        )
    )

    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)


def new_request_id() -> str:
    return uuid.uuid4().hex[:12]


def log_json(logger: logging.Logger, level: int, event: str, **payload: Any) -> None:
    safe_payload = {"event": event, **payload}
    logger.log(level, json.dumps(safe_payload, ensure_ascii=False, default=str))


def summarize_text(value: str, *, limit: int = 700) -> str:
    normalized = " ".join(value.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def elapsed_ms(start: float) -> int:
    return int((time.perf_counter() - start) * 1000)
