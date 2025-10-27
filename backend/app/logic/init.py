# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from functools import lru_cache

from punq import Container, Scope

from infrastructure.repositories.simulations.base import BaseSimulationRepository
from infrastructure.repositories.simulations.memory import MemorySimulationRepository
from logic.commands.simulations import (
    CreateSimulationCommand,
    CreateSimulationCommandHandler,
)
from logic.mediator.base import Mediator


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(
        BaseSimulationRepository, MemorySimulationRepository, scope=Scope.singleton
    )
    container.register(CreateSimulationCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateSimulationCommand, [container.resolve(CreateSimulationCommandHandler)]
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container