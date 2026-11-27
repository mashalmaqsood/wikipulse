import asyncio

from app.config import settings
from app.services.pulse_summary import PulseSummarizer

STATS = {"global": {"edits_per_minute": 12.0, "top_pages": [{"title": "Mars", "count": 3}]}}


def test_caches_summary_within_refresh_window(monkeypatch):
    calls = []

    async def fake_complete(_settings, _messages, **_kwargs):
        calls.append(1)
        return "Mars is trending."

    monkeypatch.setattr("app.services.pulse_summary.complete", fake_complete)

    summarizer = PulseSummarizer()

    first = asyncio.run(summarizer.get_summary(settings, STATS))
    second = asyncio.run(summarizer.get_summary(settings, STATS))

    assert first == "Mars is trending."
    assert second == "Mars is trending."
    assert len(calls) == 1


def test_falls_back_to_previous_summary_when_llm_fails(monkeypatch):
    responses = iter(["Mars is trending.", None])

    async def fake_complete(_settings, _messages, **_kwargs):
        return next(responses)

    monkeypatch.setattr("app.services.pulse_summary.complete", fake_complete)
    monkeypatch.setattr("app.services.pulse_summary.SUMMARY_REFRESH_SECONDS", 0.0)

    summarizer = PulseSummarizer()

    first = asyncio.run(summarizer.get_summary(settings, STATS))
    second = asyncio.run(summarizer.get_summary(settings, STATS))

    assert first == "Mars is trending."
    assert second == "Mars is trending."
