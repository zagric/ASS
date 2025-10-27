# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections import defaultdict
from collections.abc import Iterable
from dataclasses import dataclass, field
from typing import Any

from domain.events.base import BaseEvent
from logic.commands.base import BaseCommand, CommandHandler
from logic.events.base import EventHandler
from logic.exceptions.mediator import CommandHandlersNotRegisteredError


@dataclass(eq=False)
class Mediator[ET: type(BaseEvent), ER: Any, CT: type(BaseCommand), CR: Any]:
    events_map: dict[ET, list[EventHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )
    commands_map: dict[CT, list[CommandHandler]] = field(
        default_factory=lambda: defaultdict(list),
        kw_only=True,
    )

    def register_event(
        self,
        event: ET,
        event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
        self,
        command: CT,
        commands_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(commands_handlers)

    async def publish(self, events: Iterable[BaseEvent]) -> Iterable[ER]:
        result = []

        for event in events:
            event_type = event.__class__
            handlers: Iterable[EventHandler] = self.events_map[event_type]
            if not handlers:
                raise CommandHandlersNotRegisteredError(event_type)

            result.extend([await handler.handle(event) for handler in handlers])

        return result

    async def handle_command(self, command: BaseCommand) -> Iterable[CR]:
        command_type = command.__class__
        handlers = self.commands_map.get(command_type)

        if not handlers:
            raise CommandHandlersNotRegisteredError(command_type)

        return [await handler.handle(command) for handler in handlers]
