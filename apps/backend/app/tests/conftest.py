# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from punq import Container
import pytest

from infrastructure.repositories.simulations.base import BaseSimulationRepository
from logic.mediator.base import Mediator
from tests.fixtures import init_dummy_container


@pytest.fixture
def container() -> Container:
    return init_dummy_container()


@pytest.fixture
def mediator(container: Container) -> Mediator:
    return container.resolve(Mediator)


@pytest.fixture
def simulation_repository(container: Container) -> BaseSimulationRepository:
    return container.resolve(BaseSimulationRepository)
