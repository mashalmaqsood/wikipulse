import httpx

from app.config import Settings

REQUEST_TIMEOUT_SECONDS = 10.0


async def complete(settings: Settings, messages: list[dict], *, json_mode: bool = False) -> str | None:
    if not settings.llm_api_key:
        return None

    payload = {
        "model": settings.llm_model,
        "messages": messages,
        "temperature": 0.3,
        "max_completion_tokens": 300,
    }
    if json_mode:
        payload["response_format"] = {"type": "json_object"}

    headers = {"Authorization": f"Bearer {settings.llm_api_key}"}

    try:
        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            response = await client.post(settings.llm_api_url, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    except (httpx.HTTPError, KeyError, IndexError):
        return None
