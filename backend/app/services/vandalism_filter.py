import re

from app.models.events import RecentChangeEvent

IP_PATTERN = re.compile(r"^(\d{1,3}\.){3}\d{1,3}$|^[0-9a-fA-F]*:[0-9a-fA-F:]+$")
LARGE_DELETION_THRESHOLD = -500
LARGE_CHANGE_WITHOUT_COMMENT_THRESHOLD = 1000


def looks_suspicious(event: RecentChangeEvent) -> str | None:
    if event.length_delta is not None and event.length_delta <= LARGE_DELETION_THRESHOLD:
        return "large content deletion"

    if IP_PATTERN.match(event.user):
        return "anonymous (IP-based) user"

    if (
        not event.comment.strip()
        and event.length_delta is not None
        and abs(event.length_delta) > LARGE_CHANGE_WITHOUT_COMMENT_THRESHOLD
    ):
        return "large change with no edit summary"

    return None
