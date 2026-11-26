import asyncio

from app.config import settings
from app.services.pipeline import event_stream
from app.services.replay_stream import jsonl_lines


def test_replay_pipeline_matches_known_counts():
    async def run():
        counts = {"edit": 0, "new": 0, "log": 0, "categorize": 0}
        async for event in event_stream(
            jsonl_lines(settings.replay_file, speed=10_000, loop=False)
        ):
            counts[event.type] += 1
        return counts

    counts = asyncio.run(run())
    assert counts == {"edit": 1515, "new": 239, "log": 159, "categorize": 77}
    assert sum(counts.values()) == 1990
