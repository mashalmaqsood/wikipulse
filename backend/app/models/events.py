from pydantic import BaseModel

QUALIFYING_TYPES = {"edit", "new"}


class ChangeLength(BaseModel):
    old: int | None = None
    new: int | None = None


class RecentChangeEvent(BaseModel):
    type: str
    title: str
    wiki: str
    user: str
    bot: bool = False
    minor: bool = False
    timestamp: int
    comment: str = ""
    namespace: int = 0
    length: ChangeLength | None = None

    @property
    def length_delta(self) -> int | None:
        if self.length and self.length.old is not None and self.length.new is not None:
            return self.length.new - self.length.old
        return None

    @property
    def is_qualifying(self) -> bool:
        return self.type in QUALIFYING_TYPES
