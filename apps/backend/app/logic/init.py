# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from functools import lru_cache

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer
from punq import Container, Scope
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)
from sqlmodel.ext.asyncio.session import AsyncSession

from domain.events.simulations import NewSimulationCreatedEvent
from infrastructure.database.models.simulations import SimulationModel
from infrastructure.message_brokers.base import BaseMessageBroker
from infrastructure.message_brokers.kafka import KafkaMessageBroker
from infrastructure.repositories.simulations.base import BaseSimulationRepository
from infrastructure.repositories.simulations.postgresql import PGSimulationRepository
from logic.commands.simulations import (
    CreateSimulationCommand,
    CreateSimulationCommandHandler,
)
from logic.events.simulations import NewSimulationCreatedEventHandler
from logic.mediator.base import Mediator
from logic.mediator.event import EventMediator
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

    # Query handlers

    # Message brokers
    def create_message_broker() -> BaseMessageBroker:
        return KafkaMessageBroker(
            producer=AIOKafkaProducer(bootstrap_servers=config.kafka_url),
            consumer=AIOKafkaConsumer(
                bootstrap_servers=config.kafka_url,
                # group_id=f"chats-{uuid4()}",  # noqa: ERA001
                metadata_max_age_ms=30000,
            ),
        )

    container.register(
        BaseMessageBroker,
        factory=create_message_broker,
        scope=Scope.singleton,
    )

    # Mediator
    def init_mediator() -> Mediator:
        mediator = Mediator()

        # Command handlers
        create_simulation_handler = CreateSimulationCommandHandler(
            _mediator=mediator,
            simulation_repository=container.resolve(BaseSimulationRepository),
        )

        # Event handlers
        new_simulation_created_event_handler = NewSimulationCreatedEventHandler(
            broker_topic="new-simulation-created",
            message_broker=container.resolve(BaseMessageBroker),
        )

        # Commands
        mediator.register_command(
            CreateSimulationCommand,
            [create_simulation_handler],
        )

        # Events
        mediator.register_event(
            NewSimulationCreatedEvent,
            [new_simulation_created_event_handler],
        )

        # Queries

        return mediator

    container.register(Mediator, factory=init_mediator)
    container.register(EventMediator, factory=init_mediator)

    return container
