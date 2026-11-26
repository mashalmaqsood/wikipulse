import json

from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


def test_stream_endpoint_emits_stats_and_feed(monkeypatch):
    monkeypatch.setattr(settings, "stream_source", "replay")
    monkeypatch.setattr(settings, "replay_speed", 10_000)

    with TestClient(app) as client:
        with client.stream("GET", "/stream") as response:
            assert response.status_code == 200
            for line in response.iter_lines():
                if line.startswith("data:"):
                    payload = json.loads(line[len("data:"):].strip())
                    assert "stats" in payload
                    assert "feed" in payload
                    assert "global" in payload["stats"]
                    assert "by_wiki" in payload["stats"]
                    break
