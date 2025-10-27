# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC, abstractmethod
from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.simulations import Simulation


@dataclass
class BaseSimulationRepository(ABC):
    @abstractmethod
    async def get_simulation_by_oid(self, oid: str) -> Simulation | None: ...

    @abstractmethod
    async def get_all_simulations(self) -> Iterable[Simulation]: ...

    @abstractmethod
    async def add_simulation(self, simulation: Simulation) -> None: ...

    @abstractmethod
    async def delete_simulation_by_oid(self, oid: str) -> None: ...
