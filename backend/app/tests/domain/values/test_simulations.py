# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import UTC, datetime

import pytest

from domain.entities.simulations import Simulation
from domain.exceptions.simulations import (
    BufferSizeMustBePositiveError,
    BufferSizeTooLongError,
    EntitiesCountMustBePositiveError,
    EntitiesCountTooLongError,
)
from domain.values.simulations import BufferSize, EntitiesCount


def test_create_buffer_failure():
    with pytest.raises(BufferSizeTooLongError):
        BufferSize(10001)

    with pytest.raises(BufferSizeMustBePositiveError):
        BufferSize(-1)


def test_create_entities_count_failure():
    with pytest.raises(EntitiesCountMustBePositiveError):
        EntitiesCount(-5)

    with pytest.raises(EntitiesCountTooLongError):
        EntitiesCount(1001)


def test_create_simulation_success():
    simulation = Simulation(
        producers_count=EntitiesCount(3),
        consumers_count=EntitiesCount(7),
        buffer_size=BufferSize(50),
    )

    assert simulation.producers_count.value == 3
    assert simulation.consumers_count.value == 7
    assert simulation.buffer_size.value == 50
    assert simulation.created_at.date() == datetime.now(tz=UTC).date()


def test_new_simulation_events(): ...
