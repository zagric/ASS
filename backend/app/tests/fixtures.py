# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from punq import Container, Scope

from infrastructure.repositories.simulations.base import BaseSimulationRepository
from infrastructure.repositories.simulations.memory import MemorySimulationRepository
from logic.init import _init_container  # noqa: PLC2701


def init_dummy_container() -> Container:
    container = _init_container()
    container.register(
        BaseSimulationRepository,
        MemorySimulationRepository,
        scope=Scope.singleton,
    )

    return container
