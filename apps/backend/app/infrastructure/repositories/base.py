# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from abc import ABC
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from dataclasses import dataclass

from sqlalchemy import Select, Sequence
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlmodel import SQLModel, select
from sqlmodel.ext.asyncio.session import AsyncSession


@dataclass
class BaseSQLRepository[T: type(SQLModel)](ABC):
    _model: T
    _session_factory: async_sessionmaker[AsyncSession]

    @asynccontextmanager
    async def _get_session(self) -> AsyncGenerator[AsyncSession]:
        async with self._session_factory() as session:
            try:
                yield session
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    def _construct_get_stmt(self, oid: int) -> Select:
        return select(self._model).where(self._model.id == oid)

    async def get_by_id(self, oid: int) -> T | None:
        async with self._get_session() as session:
            stmt = self._construct_get_stmt(oid)
            result = await session.exec(stmt)
            return result.first()

    def _construct_list_stmt(self) -> Select:
        return select(self._model)

    async def list(self) -> Sequence[T]:
        async with self._get_session() as session:
            stmt = self._construct_list_stmt()
            results = await session.exec(stmt)
            return results.all()

    async def add(self, record: T) -> T:
        async with self._get_session() as session:
            session.add(record)
            await session.flush()
            await session.refresh(record)
            return record

    async def update(self, record: T) -> T:
        async with self._get_session() as session:
            session.add(record)
            await session.flush()
            await session.refresh(record)
            return record

    async def delete(self, oid: int) -> None:
        record = self.get_by_id(oid)
        if record is not None:
            async with self._get_session() as session:
                await session.delete(record)
                await session.flush()
