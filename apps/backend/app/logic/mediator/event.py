# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from domain.events.base import BaseEvent
from logic.events.base import EventHandler


@dataclass(eq=False)
class EventMediator[ET: BaseEvent, ER: Any](ABC):
    events_map: dict[type(ET), list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    @abstractmethod
    def register_event(
        self, event: ET, event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None: ...

    @abstractmethod
    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        ...
