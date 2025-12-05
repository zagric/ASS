# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from logic.mediator.event import EventMediator


@dataclass(frozen=True)
class BaseCommand(ABC):  # noqa: B024
    ...


@dataclass(frozen=True)
class CommandHandler[CT: BaseCommand, CR: Any](ABC):
    _mediator: EventMediator

    @abstractmethod
    async def handle(self, command: CT) -> CR:
        ...
