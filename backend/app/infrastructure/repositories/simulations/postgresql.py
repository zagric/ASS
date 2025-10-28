# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import Iterable
from dataclasses import dataclass

from domain.entities.simulations import Simulation
from infrastructure.database.models.simulations import SimulationModel
from infrastructure.repositories.base import BaseSQLRepository
from infrastructure.repositories.simulations.base import BaseSimulationRepository
from infrastructure.repositories.simulations.converters import (
    convert_simulation_entity_to_model,
)


@dataclass
class PGSimulationRepository(
    BaseSimulationRepository,
    BaseSQLRepository[SimulationModel],
):
    async def get_simulation_by_oid(self, oid: str) -> Simulation | None:
        pass

    async def get_all_simulations(self) -> Iterable[Simulation]:
        pass

    async def add_simulation(self, simulation: Simulation) -> None:
        await self.add(convert_simulation_entity_to_model(simulation))

    async def delete_simulation_by_oid(self, oid: str) -> None:
        pass
