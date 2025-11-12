# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from functools import lru_cache

from punq import Container, Scope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from infrastructure.database.models.simulations import SimulationModel
from infrastructure.repositories.simulations.base import BaseSimulationRepository
from infrastructure.repositories.simulations.postgresql import PGSimulationRepository
from logic.commands.simulations import (
    CreateSimulationCommand,
    CreateSimulationCommandHandler,
)
from logic.mediator.base import Mediator
from settings.config import Config


@lru_cache(1)
def init_container() -> Container:
    return _init_container()


def _init_container() -> Container:
    container = Container()

    container.register(Config, instance=Config(), scope=Scope.singleton)
    config: Config = container.resolve(Config)

    def create_db_engine() -> AsyncEngine:
        return create_async_engine(config.pg_connection_uri, echo=True, future=True)

    container.register(AsyncEngine, factory=create_db_engine, scope=Scope.singleton)
    engine: AsyncEngine = container.resolve(AsyncEngine)

    def create_session_factory() -> async_sessionmaker[AsyncSession]:
        print("Creating session factory")
        return async_sessionmaker(
            engine,
            expire_on_commit=False,
            autoflush=False,
        )

    def init_simulation_repository() -> BaseSimulationRepository:
        return PGSimulationRepository(
            _session_factory=create_session_factory(),
            _model=SimulationModel,
        )

    container.register(
        BaseSimulationRepository,
        factory=init_simulation_repository,
        scope=Scope.singleton,
    )
    container.register(CreateSimulationCommandHandler)

    def init_mediator() -> Mediator:
        mediator = Mediator()
        mediator.register_command(
            CreateSimulationCommand,
            [container.resolve(CreateSimulationCommandHandler)],
        )

        return mediator

    container.register(Mediator, factory=init_mediator)

    return container
