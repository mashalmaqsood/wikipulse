import time

from app.config import Settings
from app.services.ai_client import complete

SUMMARY_REFRESH_SECONDS = 60.0

SYSTEM_PROMPT = (
    "You summarize live Wikipedia edit activity in 2-3 short, plain-English "
    "sentences. No markdown, no bullet points, just prose."
)


class PulseSummarizer:
    def __init__(self) -> None:
        self._cached_text: str | None = None
        self._cached_at: float = 0.0

    async def get_summary(self, settings: Settings, stats: dict) -> str | None:
        now = time.monotonic()
        if self._cached_text is not None and now - self._cached_at < SUMMARY_REFRESH_SECONDS:
            return self._cached_text

        text = await complete(
            settings,
            [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": _build_prompt(stats)},
            ],
        )

        if text is not None:
            self._cached_text = text
            self._cached_at = now

        return self._cached_text


def _build_prompt(stats: dict) -> str:
    global_stats = stats.get("global", {})
    top_pages = global_stats.get("top_pages", [])[:5]
    edits_per_minute = global_stats.get("edits_per_minute", 0)

    pages_text = ", ".join(f"{p['title']} ({p['count']} edits)" for p in top_pages)
    if not pages_text:
        pages_text = "no notable pages yet"

    return (
        f"Current edit rate: {edits_per_minute} edits/minute.\n"
        f"Most-edited pages in the last 5 minutes: {pages_text}.\n"
        "What's trending right now?"
    )
