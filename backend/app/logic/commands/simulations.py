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
class CreateSimulationCommandHandler(CommandHandler[CreateSimulationCommand, Simulation]):
    simulation_repository: BaseSimulationRepository

    async def handle(self, command: CreateSimulationCommand) -> Simulation:
        producers_count = EntitiesCount(command.producers_count)
        consumers_count = EntitiesCount(command.consumers_count)
        buffer_size = BufferSize(command.buffer_size)

        new_simulation = Simulation.create_simulation(producers_count, consumers_count, buffer_size)

        await self.simulation_repository.add_simulation(new_simulation)
        
        return new_simulation

