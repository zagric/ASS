# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import Iterable
from dataclasses import dataclass, field

from domain.entities.simulations import Simulation
from infrastructure.repositories.simulations.base import BaseSimulationRepository


@dataclass
class MemorySimulationRepository(BaseSimulationRepository):
    _saved_simulations: list[Simulation] = field(default_factory=list, kw_only=True)

    async def get_simulation_by_oid(self, oid: str) -> Simulation | None:
        try:
            return next(
                simulation
                for simulation in self._saved_simulations
                if simulation.oid == oid
            )
        except StopIteration:
            return None

    async def get_all_simulations(self) -> Iterable[Simulation]:
        raise NotImplementedError

    async def add_simulation(self, simulation: Simulation) -> None:
        self._saved_simulations.append(simulation)

    async def delete_simulation_by_oid(self, oid: str) -> None:
        raise NotImplementedError
