# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from punq import Container

from application.api.schemas import ErrorSchema
from application.api.simulations.schemas import (
    CreateSimulationRequestSchema,
    CreateSimulationResponseSchema,
)
from domain.exceptions.base import ApplicationError
from logic.commands.simulations import CreateSimulationCommand
from logic.init import init_container
from logic.mediator.base import Mediator


router = APIRouter(tags=["Simulation"])


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    responses={
        status.HTTP_201_CREATED: {"model": CreateSimulationResponseSchema},
        status.HTTP_400_BAD_REQUEST: {"model": ErrorSchema},
    },
    summary="Create a new simulation",
)
async def create_simulation_handler(
    schema: CreateSimulationRequestSchema,
    container: Annotated[Container, Depends(init_container)],
) -> CreateSimulationResponseSchema:
    """Initiate a new simulation with specified parameters."""  # noqa: DOC201, DOC501
    mediator: Mediator = container.resolve(Mediator)

    try:
        simulation, *_ = await mediator.handle_command(
            CreateSimulationCommand(
                producers_count=schema.producers_count,
                consumers_count=schema.consumers_count,
                buffer_size=schema.buffer_size,
            ),
        )
    except ApplicationError as error:
        raise HTTPException(status_code=400, detail={"error": error.message}) from error

    return CreateSimulationResponseSchema.from_entity(simulation)
