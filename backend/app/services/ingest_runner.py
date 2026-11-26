from app.config import Settings
from app.services.feed_buffer import FeedBuffer
from app.services.pipeline import event_stream, raw_line_source
from app.services.stats_engine import StatsEngine


async def run_ingestion(settings: Settings, stats_engine: StatsEngine, feed_buffer: FeedBuffer) -> None:
    async for event in event_stream(raw_line_source(settings)):
        stats_engine.record(event)
        feed_buffer.add(event)
