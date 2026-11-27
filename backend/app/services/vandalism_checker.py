import json

from app.config import Settings
from app.models.events import RecentChangeEvent
from app.services.ai_client import complete
from app.services.vandalism_filter import looks_suspicious

SYSTEM_PROMPT = (
    "You are a careful Wikipedia edit reviewer. Decide whether an edit looks "
    "like vandalism. Never claim certainty you don't have -- use \"uncertain\" "
    "when evidence is weak. Respond with JSON only: "
    '{"verdict": "vandalism" | "clean" | "uncertain", "reason": "<short reason>"}'
)


async def check_vandalism(settings: Settings, event: RecentChangeEvent) -> dict | None:
    rule_reason = looks_suspicious(event)
    if rule_reason is None:
        return None

    prompt = (
        f'Edit to "{event.title}" by user "{event.user}" (bot={event.bot}).\n'
        f'Comment: "{event.comment}"\n'
        f"Content size change: {event.length_delta}\n"
        f"A rule-based filter flagged this edit because: {rule_reason}."
    )

    text = await complete(
        settings,
        [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        json_mode=True,
    )

    if text is None:
        return {"verdict": "uncertain", "reason": rule_reason}

    try:
        parsed = json.loads(text)
        return {
            "verdict": parsed.get("verdict", "uncertain"),
            "reason": parsed.get("reason", rule_reason),
        }
    except (json.JSONDecodeError, AttributeError):
        return {"verdict": "uncertain", "reason": rule_reason}
