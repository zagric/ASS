# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.simulations import NewSimulationCreatedEvent
from domain.values.simulations import BufferSize, Duration, EntitiesCount, RequestRate


@dataclass(eq=False)
class Simulation(BaseEntity):
    producers_count: EntitiesCount
    consumers_count: EntitiesCount
    buffer_size: BufferSize
    simulation_duration: Duration
    request_rate: RequestRate

    @classmethod
    def create_simulation(
        cls,
        prod_count: EntitiesCount,
        cons_count: EntitiesCount,
        buff_size: BufferSize,
        simulation_duration: Duration,
        request_rate: RequestRate,
    ) -> "Simulation":
        new_simulation = cls(
            producers_count=prod_count,
            consumers_count=cons_count,
            buffer_size=buff_size,
            simulation_duration=simulation_duration,
            request_rate=request_rate,
        )
        new_simulation.register_event(
            NewSimulationCreatedEvent(
                simulation_oid=new_simulation.oid,
                producers_count=prod_count.as_generic_type(),
                consumers_count=cons_count.as_generic_type(),
                buffer_size=buff_size.as_generic_type(),
                simulation_duration=simulation_duration.as_generic_type(),
                request_rate=request_rate.as_generic_type(),
            ),
        )

        return new_simulation
