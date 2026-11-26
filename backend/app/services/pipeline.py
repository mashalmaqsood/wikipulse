import json
import logging
from typing import AsyncIterator

from pydantic import ValidationError

from app.config import Settings
from app.models.events import RecentChangeEvent
from app.services.live_stream import sse_lines
from app.services.replay_stream import jsonl_lines

logger = logging.getLogger(__name__)


async def event_stream(raw_lines: AsyncIterator[str]) -> AsyncIterator[RecentChangeEvent]:
    async for line in raw_lines:
        line = line.strip()
        if not line:
            continue
        try:
            data = json.loads(line)
        except json.JSONDecodeError:
            logger.warning("Skipping malformed JSON line: %.200s", line)
            continue
        try:
            event = RecentChangeEvent.model_validate(data)
        except ValidationError as exc:
            logger.warning("Skipping invalid event (%s): %.200s", exc.errors()[0]["msg"], line)
            continue
        yield event


def raw_line_source(settings: Settings) -> AsyncIterator[str]:
    if settings.stream_source == "replay":
        return jsonl_lines(settings.replay_file, speed=settings.replay_speed, loop=settings.replay_loop)
    return sse_lines(settings.wikipedia_stream_url)
