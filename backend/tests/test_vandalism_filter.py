from app.models.events import RecentChangeEvent
from app.services.vandalism_filter import looks_suspicious


def _event(user: str, comment: str, old: int, new: int) -> RecentChangeEvent:
    return RecentChangeEvent(
        type="edit",
        title="Mars",
        wiki="enwiki",
        user=user,
        comment=comment,
        timestamp=0,
        length={"old": old, "new": new},
    )


def test_normal_edit_is_not_flagged():
    event = _event("ExampleEditor001", "Fixed a typo", 1000, 1010)
    assert looks_suspicious(event) is None


def test_large_deletion_is_flagged():
    event = _event("ExampleEditor001", "Cleanup", 2000, 100)
    assert looks_suspicious(event) == "large content deletion"


def test_anonymous_ip_user_is_flagged():
    event = _event("203.0.113.42", "edit", 1000, 1010)
    assert looks_suspicious(event) == "anonymous (IP-based) user"


def test_large_change_without_comment_is_flagged():
    event = _event("ExampleEditor001", "", 1000, 3000)
    assert looks_suspicious(event) == "large change with no edit summary"
