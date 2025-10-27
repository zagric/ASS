# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.entities.simulations import Simulation
from domain.values.simulations import BufferSize, EntitiesCount
from infrastructure.repositories.simulations.base import BaseSimulationRepository
from logic.commands.base import BaseCommand, CommandHandler


@dataclass(frozen=True)
class CreateSimulationCommand(BaseCommand):
    producers_count: int
    consumers_count: int
    buffer_size: int


@dataclass(frozen=True)
class CreateSimulationCommandHandler(
    CommandHandler[CreateSimulationCommand, Simulation],
):
    simulation_repository: BaseSimulationRepository

    async def handle(self, command: CreateSimulationCommand) -> Simulation:
        producers_count = EntitiesCount(command.producers_count)
        consumers_count = EntitiesCount(command.consumers_count)
        buffer_size = BufferSize(command.buffer_size)

        new_simulation = Simulation.create_simulation(
            producers_count,
            consumers_count,
            buffer_size,
        )

        await self.simulation_repository.add_simulation(new_simulation)

        return new_simulation
