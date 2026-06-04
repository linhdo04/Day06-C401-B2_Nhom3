from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    repo_root = Path(__file__).resolve().parents[2]
    for env_file in (
        repo_root / ".env",
        repo_root / "backend" / ".env",
        repo_root / "frontend" / ".env.local",
        repo_root / "frontend" / ".env",
        repo_root / "tests" / "e2e" / ".env",
    ):
        if env_file.exists():
            load_dotenv(env_file, override=False)
