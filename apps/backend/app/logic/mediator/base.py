# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import Iterable
from dataclasses import dataclass
from typing import Any

from domain.events.base import BaseEvent
from logic.commands.base import BaseCommand, CommandHandler
from logic.events.base import EventHandler
from logic.exceptions.mediator import CommandHandlersNotRegisteredError
from logic.mediator.command import CommandMediator
from logic.mediator.event import EventMediator
from logic.mediator.query import QueryMediator
from logic.queries.base import BaseQuery, BaseQueryHandler


@dataclass(eq=False)
class Mediator[
    ET: BaseEvent,
    ER: Any,
    CT: BaseCommand,
    CR: Any,
    QT: BaseQuery,
    QR: Any,
](
    EventMediator[ET, ER],
    CommandMediator[CT, CR],
    QueryMediator[QT, QR],
):
    def register_event(
        self,
        event: type(ET),
        event_handlers: Iterable[EventHandler[ET, ER]],
    ) -> None:
        self.events_map[event].extend(event_handlers)

    def register_command(
        self,
        command: type(CT),
        commands_handlers: Iterable[CommandHandler[CT, CR]],
    ) -> None:
        self.commands_map[command].extend(commands_handlers)

    def register_query(
        self, query: type(QT), query_handler: BaseQueryHandler[QT, QR],
    ) -> QR:
        self.queries_map[query] = query_handler

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

    async def handle_query(self, query: BaseQuery) -> QR:
        return await self.queries_map[query.__class__].handle(query)
