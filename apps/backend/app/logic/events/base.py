# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from domain.events.base import BaseEvent


@dataclass
class EventHandler[ET: BaseEvent, ER: Any](ABC):
    @abstractmethod
    def handle(self, event: ET) -> ER:
        ...
