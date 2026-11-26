import asyncio
import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import settings
from app.services.feed_buffer import FeedBuffer
from app.services.ingest_runner import run_ingestion
from app.services.stats_engine import StatsEngine

BROADCAST_INTERVAL_SECONDS = 1.5


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.stats_engine = StatsEngine()
    app.state.feed_buffer = FeedBuffer()
    task = asyncio.create_task(run_ingestion(settings, app.state.stats_engine, app.state.feed_buffer))
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass


app = FastAPI(title="WikiPulse API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/stream")
async def stream(request: Request) -> StreamingResponse:
    async def event_generator():
        while True:
            payload = {
                "stats": request.app.state.stats_engine.snapshot(),
                "feed": request.app.state.feed_buffer.recent(),
            }
            yield f"data: {json.dumps(payload)}\n\n"
            await asyncio.sleep(BROADCAST_INTERVAL_SECONDS)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
