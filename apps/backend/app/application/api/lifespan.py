# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from typing import TYPE_CHECKING

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import SQLModel

from infrastructure.message_brokers.base import BaseMessageBroker
from logic.init import init_container


if TYPE_CHECKING:
    from punq import Container


async def init_db() -> None:
    container: Container = init_container()
    engine: AsyncEngine = container.resolve(AsyncEngine)

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)
        await conn.run_sync(SQLModel.metadata.create_all)


async def init_message_broker() -> None:
    container: Container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.start()


async def close_message_broker() -> None:
    container: Container = init_container()
    message_broker: BaseMessageBroker = container.resolve(BaseMessageBroker)
    await message_broker.close()
