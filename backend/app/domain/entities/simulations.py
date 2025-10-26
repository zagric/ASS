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

from domain.entities.base import BaseEntity
from domain.events.simulations import NewSimulationCreatedEvent
from domain.values.simulations import BufferSize, EntitiesCount


@dataclass(eq=False)
class Simulation(BaseEntity):
    producers_count: EntitiesCount
    consumers_count: EntitiesCount
    buffer_size: BufferSize

    @classmethod
    def create_simulation(cls, prod_count: EntitiesCount, cons_count: EntitiesCount, buff_size: BufferSize) -> "Simulation":
        new_simulation = cls(
            producers_count=prod_count,
            consumers_count=cons_count,
            buffer_size=buff_size,
        )
        new_simulation.register_event(NewSimulationCreatedEvent(simulation_oid=new_simulation.oid))
        
        return new_simulation