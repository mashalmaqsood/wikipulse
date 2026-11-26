import asyncio

from app.config import settings
from app.services.feed_buffer import FeedBuffer
from app.services.ingest_runner import run_ingestion
from app.services.stats_engine import MIN_ELAPSED_SECONDS, StatsEngine


def test_ingestion_populates_stats_and_feed():
    replay_settings = settings.model_copy(
        update={"stream_source": "replay", "replay_speed": 10_000, "replay_loop": False}
    )

    stats_engine = StatsEngine()
    feed_buffer = FeedBuffer()

    asyncio.run(run_ingestion(replay_settings, stats_engine, feed_buffer))

    stats_engine._started_at -= MIN_ELAPSED_SECONDS + 1
    snapshot = stats_engine.snapshot()

    assert snapshot["global"]["edits_per_minute"] > 0
    assert len(snapshot["global"]["top_pages"]) > 0
    assert len(feed_buffer.recent()) > 0
