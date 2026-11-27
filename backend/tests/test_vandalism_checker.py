import asyncio
import json

from app.config import settings
from app.models.events import RecentChangeEvent
from app.services.vandalism_checker import check_vandalism


def _event(user: str = "ExampleEditor001", old: int = 1000, new: int = 50) -> RecentChangeEvent:
    return RecentChangeEvent(
        type="edit",
        title="Mars",
        wiki="enwiki",
        user=user,
        comment="",
        timestamp=0,
        length={"old": old, "new": new},
    )


def test_clean_edit_skips_llm_entirely(monkeypatch):
    called = []

    async def fake_complete(*_args, **_kwargs):
        called.append(1)
        return "{}"

    monkeypatch.setattr("app.services.vandalism_checker.complete", fake_complete)

    event = RecentChangeEvent(
        type="edit", title="Mars", wiki="enwiki", user="ExampleEditor001",
        comment="Fixed a typo", timestamp=0, length={"old": 1000, "new": 1010},
    )
    result = asyncio.run(check_vandalism(settings, event))

    assert result is None
    assert called == []


def test_flagged_edit_parses_llm_verdict(monkeypatch):
    async def fake_complete(*_args, **_kwargs):
        return json.dumps({"verdict": "vandalism", "reason": "mass content removal"})

    monkeypatch.setattr("app.services.vandalism_checker.complete", fake_complete)

    result = asyncio.run(check_vandalism(settings, _event()))

    assert result == {"verdict": "vandalism", "reason": "mass content removal"}


def test_flagged_edit_falls_back_when_llm_unavailable(monkeypatch):
    async def fake_complete(*_args, **_kwargs):
        return None

    monkeypatch.setattr("app.services.vandalism_checker.complete", fake_complete)

    result = asyncio.run(check_vandalism(settings, _event()))

    assert result == {"verdict": "uncertain", "reason": "large content deletion"}


def test_flagged_edit_falls_back_on_malformed_json(monkeypatch):
    async def fake_complete(*_args, **_kwargs):
        return "not valid json"

    monkeypatch.setattr("app.services.vandalism_checker.complete", fake_complete)

    result = asyncio.run(check_vandalism(settings, _event()))

    assert result == {"verdict": "uncertain", "reason": "large content deletion"}
