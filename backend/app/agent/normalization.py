from __future__ import annotations

import unicodedata


def normalize_text(value: str) -> str:
    text = value.strip().lower().replace("đ", "d")
    text = unicodedata.normalize("NFD", text)
    without_marks = "".join(char for char in text if unicodedata.category(char) != "Mn")
    return " ".join(without_marks.replace("-", " ").split())


CITY_ALIASES = {
    "ha noi": "ha noi",
    "hanoi": "ha noi",
    "hn": "ha noi",
    "da nang": "da nang",
    "danang": "da nang",
    "dn": "da nang",
    "hue": "hue",
    "nha trang": "nha trang",
    "ho chi minh": "ho chi minh",
    "sai gon": "ho chi minh",
    "saigon": "ho chi minh",
    "hcm": "ho chi minh",
    "tp hcm": "ho chi minh",
}


def normalize_city(value: str) -> str:
    normalized = normalize_text(value)
    return CITY_ALIASES.get(normalized, normalized)
