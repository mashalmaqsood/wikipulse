from collections import deque
from typing import NamedTuple

from app.models.events import RecentChangeEvent

MAX_FEED_ITEMS = 50


class FeedItem(NamedTuple):
    type: str
    title: str
    wiki: str
    user: str
    bot: bool
    comment: str
    length_delta: int | None


class FeedBuffer:
    def __init__(self) -> None:
        self._items: deque[FeedItem] = deque(maxlen=MAX_FEED_ITEMS)

    def add(self, event: RecentChangeEvent) -> None:
        if not event.is_qualifying:
            return
        self._items.appendleft(
            FeedItem(
                type=event.type,
                title=event.title,
                wiki=event.wiki,
                user=event.user,
                bot=event.bot,
                comment=event.comment,
                length_delta=event.length_delta,
            )
        )

    def recent(self) -> list[dict]:
        return [item._asdict() for item in self._items]
