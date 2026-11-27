import asyncio

from app.config import settings
from app.services.ai_client import complete


def test_returns_none_without_api_key_and_makes_no_network_call():
    no_key_settings = settings.model_copy(update={"llm_api_key": ""})

    result = asyncio.run(complete(no_key_settings, [{"role": "user", "content": "hi"}]))

    assert result is None
