# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from logic.exceptions.base import LogicError


@dataclass(eq=False)
class EventHandlersNotRegisteredError(LogicError):
    event_type: type

    @property
    def message(self) -> str:
        return f"Event handlers could not be found for: {self.event_type}"


@dataclass(eq=False)
class CommandHandlersNotRegisteredError(LogicError):
    command_type: type

    @property
    def message(self) -> str:
        return f"Command handlers could not be found for: {self.command_type}"
