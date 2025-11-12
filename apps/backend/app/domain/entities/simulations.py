# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from dataclasses import dataclass

from domain.entities.base import BaseEntity
from domain.events.simulations import NewSimulationCreatedEvent
from domain.values.simulations import BufferSize, EntitiesCount


@dataclass(eq=False)
class Simulation(BaseEntity):
    producers_count: EntitiesCount
    consumers_count: EntitiesCount
    buffer_size: BufferSize

    @classmethod
    def create_simulation(
        cls,
        prod_count: EntitiesCount,
        cons_count: EntitiesCount,
        buff_size: BufferSize,
    ) -> "Simulation":
        new_simulation = cls(
            producers_count=prod_count,
            consumers_count=cons_count,
            buffer_size=buff_size,
        )
        new_simulation.register_event(
            NewSimulationCreatedEvent(simulation_oid=new_simulation.oid),
        )

        return new_simulation
