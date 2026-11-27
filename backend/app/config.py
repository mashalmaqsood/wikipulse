from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    wikipedia_stream_url: str = "https://stream.wikimedia.org/v2/stream/recentchange"
    frontend_origin: str = "http://localhost:5173"

    llm_api_key: str = ""
    llm_model: str = ""
    llm_api_url: str = "https://api.groq.com/openai/v1/chat/completions"

    # "live" talks to Wikimedia's real SSE stream; "replay" paces through
    # sample_events.jsonl so the dashboard behaves identically with no network access.
    stream_source: str = "live"
    replay_file: Path = PROJECT_ROOT / "sample_events.jsonl"
    replay_speed: float = 1.0
    replay_loop: bool = True


settings = Settings()
