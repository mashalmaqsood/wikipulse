import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import AsyncIterator

MAX_GAP_SECONDS = 5.0


async def jsonl_lines(path: Path, speed: float = 1.0, loop: bool = True) -> AsyncIterator[str]:
    while True:
        prev_dt: datetime | None = None
        with open(path, "r", encoding="utf-8") as f:
            for raw_line in f:
                line = raw_line.rstrip("\n")
                if not line:
                    continue
                dt = _extract_dt(line)
                if prev_dt is not None and dt is not None:
                    delay = min((dt - prev_dt).total_seconds(), MAX_GAP_SECONDS) / speed
                    if delay > 0.001:
                        await asyncio.sleep(delay)
                if dt is not None:
                    prev_dt = dt
                yield line
        if not loop:
            return


def _extract_dt(line: str) -> datetime | None:
    try:
        data = json.loads(line)
        return datetime.fromisoformat(data["meta"]["dt"].replace("Z", "+00:00"))
    except Exception:
        return None
