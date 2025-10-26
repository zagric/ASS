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
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable

from domain.entities.simulations import Simulation


@dataclass
class BaseSimulationRepository(ABC):
    @abstractmethod
    async def get_simulation_by_oid(self, oid: str) -> Simulation | None:
        ...

    @abstractmethod
    async def get_all_simulations(self) -> Iterable[Simulation]:
        ...

    @abstractmethod
    async def add_simulation(self, simulation: Simulation) -> None:
        ...

    @abstractmethod
    async def delete_simulation_by_oid(self, oid: str) -> None:
        ...