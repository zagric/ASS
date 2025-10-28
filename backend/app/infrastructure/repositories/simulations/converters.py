# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from domain.entities.simulations import Simulation
from domain.values.simulations import BufferSize, EntitiesCount
from infrastructure.database.models.simulations import SimulationModel


def convert_simulation_entity_to_model(simulation: Simulation) -> SimulationModel:
    return SimulationModel(
        oid=simulation.oid,
        producers_count=simulation.producers_count.value,
        consumers_count=simulation.consumers_count.value,
        buffer_size=simulation.buffer_size.value,
        created_at=simulation.created_at,
    )


def convert_model_to_simulation_entity(model: SimulationModel) -> Simulation:
    return Simulation(
        oid=model.oid,
        producers_count=EntitiesCount(model.producers_count),
        consumers_count=EntitiesCount(model.consumers_count),
        buffer_size=BufferSize(model.buffer_size),
        created_at=model.created_at,
    )
