# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import datetime

from pydantic import BaseModel

from domain.entities.simulations import Simulation


class CreateSimulationRequestSchema(BaseModel):
    producers_count: int
    consumers_count: int
    buffer_size: int
    simulation_duration: int
    request_rate: float


class CreateSimulationResponseSchema(BaseModel):
    oid: str
    producers_count: int
    consumers_count: int
    buffer_size: int
    simulation_duration: int
    request_rate: float
    created_at: datetime

    @classmethod
    def from_entity(cls, simulation: Simulation) -> "CreateSimulationResponseSchema":
        return CreateSimulationResponseSchema(
            oid=simulation.oid,
            producers_count=simulation.producers_count.as_generic_type(),
            consumers_count=simulation.consumers_count.as_generic_type(),
            buffer_size=simulation.buffer_size.as_generic_type(),
            simulation_duration=simulation.simulation_duration.as_generic_type(),
            request_rate=simulation.request_rate.as_generic_type(),
            created_at=simulation.created_at,
        )
