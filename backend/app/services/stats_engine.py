import time
from collections import Counter, deque
from typing import NamedTuple

from app.models.events import RecentChangeEvent

WINDOW_SECONDS = 300.0
TOP_PAGES_LIMIT = 10
MIN_ELAPSED_SECONDS = 5.0


class _Record(NamedTuple):
    arrival_time: float
    wiki: str
    title: str


class StatsEngine:
    def __init__(self) -> None:
        self._records: deque[_Record] = deque()
        self._started_at = time.monotonic()

    def record(self, event: RecentChangeEvent) -> None:
        if not event.is_qualifying:
            return
        self._records.append(_Record(time.monotonic(), event.wiki, event.title))

    def snapshot(self) -> dict:
        self._evict_stale()

        elapsed_seconds = time.monotonic() - self._started_at
        if elapsed_seconds < MIN_ELAPSED_SECONDS:
            elapsed_minutes = 0.0
        else:
            elapsed_minutes = min(elapsed_seconds, WINDOW_SECONDS) / 60.0

        return {
            "global": self._compute(self._records, elapsed_minutes),
            "by_wiki": {
                wiki: self._compute(records, elapsed_minutes)
                for wiki, records in self._group_by_wiki().items()
            },
        }

    def _evict_stale(self) -> None:
        cutoff = time.monotonic() - WINDOW_SECONDS
        while self._records and self._records[0].arrival_time < cutoff:
            self._records.popleft()

    def _group_by_wiki(self) -> dict[str, list[_Record]]:
        groups: dict[str, list[_Record]] = {}
        for r in self._records:
            groups.setdefault(r.wiki, []).append(r)
        return groups

    @staticmethod
    def _compute(records, elapsed_minutes: float) -> dict:
        edits_per_minute = round(len(records) / elapsed_minutes, 2) if elapsed_minutes > 0 else 0.0
        top_pages = Counter(r.title for r in records).most_common(TOP_PAGES_LIMIT)
        return {
            "edits_per_minute": edits_per_minute,
            "top_pages": [{"title": title, "count": count} for title, count in top_pages],
        }
