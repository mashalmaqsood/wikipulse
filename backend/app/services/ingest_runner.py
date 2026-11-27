import asyncio

from app.config import Settings
from app.models.events import RecentChangeEvent
from app.services.feed_buffer import FeedBuffer, FeedItem
from app.services.pipeline import event_stream, raw_line_source
from app.services.stats_engine import StatsEngine
from app.services.vandalism_checker import check_vandalism


async def run_ingestion(settings: Settings, stats_engine: StatsEngine, feed_buffer: FeedBuffer) -> None:
    async for event in event_stream(raw_line_source(settings)):
        stats_engine.record(event)
        item = feed_buffer.add(event)
        if item is not None:
            asyncio.create_task(_attach_vandalism_verdict(settings, event, item))


async def _attach_vandalism_verdict(settings: Settings, event: RecentChangeEvent, item: FeedItem) -> None:
    item.vandalism = await check_vandalism(settings, event)
