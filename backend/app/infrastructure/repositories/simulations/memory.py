# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# 
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
# 
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass, field
from typing import Iterable

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
        raise NotImplementedError()

    async def add_simulation(self, simulation: Simulation) -> None:
        self._saved_simulations.append(simulation)

    async def delete_simulation_by_oid(self, oid: str) -> None:
        raise NotImplementedError()
