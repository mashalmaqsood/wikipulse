from collections import deque
from dataclasses import asdict, dataclass

from app.models.events import RecentChangeEvent

MAX_FEED_ITEMS = 50


@dataclass
class FeedItem:
    type: str
    title: str
    wiki: str
    user: str
    bot: bool
    comment: str
    length_delta: int | None
    vandalism: dict | None = None


class FeedBuffer:
    def __init__(self) -> None:
        self._items: deque[FeedItem] = deque(maxlen=MAX_FEED_ITEMS)

    def add(self, event: RecentChangeEvent) -> FeedItem | None:
        if not event.is_qualifying:
            return None
        item = FeedItem(
            type=event.type,
            title=event.title,
            wiki=event.wiki,
            user=event.user,
            bot=event.bot,
            comment=event.comment,
            length_delta=event.length_delta,
        )
        self._items.appendleft(item)
        return item

    def recent(self) -> list[dict]:
        return [asdict(item) for item in self._items]
