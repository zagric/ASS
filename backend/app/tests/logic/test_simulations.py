# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from faker import Faker
import pytest

from infrastructure.repositories.simulations.base import BaseSimulationRepository
from logic.commands.simulations import CreateSimulationCommand
from logic.mediator.base import Mediator


@pytest.mark.asyncio
async def test_create_simulation_command_success(
    simulation_repository: BaseSimulationRepository,
    mediator: Mediator,
    faker: Faker,
):
    simulation, *_ = await mediator.handle_command(
        CreateSimulationCommand(
            producers_count=faker.random_int(min=0, max=1000),
            consumers_count=faker.random_int(min=0, max=1000),
            buffer_size=faker.random_int(min=0, max=10000),
        ),
    )

    assert (
        await simulation_repository.get_simulation_by_oid(simulation.oid) == simulation
    )
    assert len(simulation_repository._saved_simulations) == 1
