from app.models.events import RecentChangeEvent
from app.services.feed_buffer import MAX_FEED_ITEMS, FeedBuffer


def _event(type_: str, title: str) -> RecentChangeEvent:
    return RecentChangeEvent(type=type_, title=title, wiki="enwiki", user="tester", timestamp=0)


def test_non_qualifying_events_are_ignored():
    buffer = FeedBuffer()
    buffer.add(_event("log", "Mars"))
    buffer.add(_event("categorize", "Mars"))

    assert buffer.recent() == []


def test_most_recent_first():
    buffer = FeedBuffer()
    buffer.add(_event("edit", "Mars"))
    buffer.add(_event("new", "Climate Change"))

    titles = [item["title"] for item in buffer.recent()]
    assert titles == ["Climate Change", "Mars"]


def test_buffer_is_capped():
    buffer = FeedBuffer()
    for i in range(MAX_FEED_ITEMS + 10):
        buffer.add(_event("edit", f"Page{i}"))

    assert len(buffer.recent()) == MAX_FEED_ITEMS
    assert buffer.recent()[0]["title"] == f"Page{MAX_FEED_ITEMS + 9}"
