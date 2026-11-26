from app.models.events import RecentChangeEvent
from app.services.stats_engine import MIN_ELAPSED_SECONDS, StatsEngine


def _event(type_: str, title: str, wiki: str = "enwiki") -> RecentChangeEvent:
    return RecentChangeEvent(
        type=type_,
        title=title,
        wiki=wiki,
        user="tester",
        timestamp=0,
    )


def test_non_qualifying_events_are_ignored():
    engine = StatsEngine()
    engine._started_at -= MIN_ELAPSED_SECONDS + 1

    engine.record(_event("log", "Mars"))
    engine.record(_event("categorize", "Mars"))
    engine.record(_event("edit", "Mars"))

    snapshot = engine.snapshot()
    assert snapshot["global"]["top_pages"] == [{"title": "Mars", "count": 1}]


def test_top_pages_and_wiki_breakdown():
    engine = StatsEngine()
    engine._started_at -= MIN_ELAPSED_SECONDS + 1

    engine.record(_event("edit", "Mars", wiki="enwiki"))
    engine.record(_event("edit", "Mars", wiki="enwiki"))
    engine.record(_event("new", "Climate Change", wiki="enwiki"))
    engine.record(_event("edit", "Erde", wiki="dewiki"))

    snapshot = engine.snapshot()

    assert snapshot["global"]["top_pages"][0] == {"title": "Mars", "count": 2}
    assert snapshot["by_wiki"]["enwiki"]["top_pages"][0] == {"title": "Mars", "count": 2}
    assert snapshot["by_wiki"]["dewiki"]["top_pages"] == [{"title": "Erde", "count": 1}]


def test_rate_is_zero_before_minimum_elapsed_time():
    engine = StatsEngine()
    engine.record(_event("edit", "Mars"))

    snapshot = engine.snapshot()

    assert snapshot["global"]["edits_per_minute"] == 0.0


def test_stale_records_are_evicted():
    from app.services import stats_engine as module

    engine = StatsEngine()
    engine._started_at -= MIN_ELAPSED_SECONDS + 1
    engine.record(_event("edit", "Mars"))

    engine._records[0] = engine._records[0]._replace(
        arrival_time=engine._records[0].arrival_time - module.WINDOW_SECONDS - 1
    )

    snapshot = engine.snapshot()
    assert snapshot["global"]["top_pages"] == []
