from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Callable


@dataclass
class Event:
    kind: str
    payload: dict[str, Any]
    ts: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Bus:
    def __init__(self) -> None:
        self._subs: list[Callable[[Event], None]] = []
        self.history: list[Event] = []

    def subscribe(self, fn: Callable[[Event], None]) -> None:
        self._subs.append(fn)

    def emit(self, kind: str, **payload: Any) -> Event:
        event = Event(kind=kind, payload=payload)
        self.history.append(event)
        for fn in self._subs:
            fn(event)
        return event
