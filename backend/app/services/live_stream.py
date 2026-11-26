import asyncio
import logging
from typing import AsyncIterator

import httpx

logger = logging.getLogger(__name__)

MAX_BACKOFF_SECONDS = 30.0
STREAM_TIMEOUT = httpx.Timeout(connect=10.0, read=None, write=10.0, pool=10.0)


async def sse_lines(url: str) -> AsyncIterator[str]:
    backoff = 1.0
    async with httpx.AsyncClient(timeout=STREAM_TIMEOUT) as client:
        while True:
            try:
                async with client.stream("GET", url, headers={"Accept": "text/event-stream"}) as response:
                    response.raise_for_status()
                    backoff = 1.0
                    data_lines: list[str] = []
                    async for line in response.aiter_lines():
                        if line == "":
                            if data_lines:
                                yield "\n".join(data_lines)
                                data_lines = []
                            continue
                        if line.startswith(":"):
                            continue
                        if line.startswith("data:"):
                            data_lines.append(line[len("data:"):].lstrip())
            except httpx.HTTPError as exc:
                logger.warning("Wikimedia stream disconnected (%s); reconnecting in %.0fs", exc, backoff)
                await asyncio.sleep(backoff)
                backoff = min(backoff * 2, MAX_BACKOFF_SECONDS)
