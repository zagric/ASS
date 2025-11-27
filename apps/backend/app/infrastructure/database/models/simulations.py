# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import UTC, datetime

from sqlalchemy import SmallInteger
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE
from sqlmodel import Field, SQLModel


class SimulationModel(SQLModel, table=True):
    __tablename__ = "simulations"

    id: int | None = Field(default=None, primary_key=True)
    oid: str = Field(index=True, unique=True)
    producers_count: int = Field(sa_type=SmallInteger, default=0)
    consumers_count: int = Field(sa_type=SmallInteger, default=0)
    buffer_size: int = Field(sa_type=SmallInteger, default=0)

    created_at: datetime = Field(
        default=datetime.now(tz=UTC), sa_type=DATETIME_TIMEZONE,
    )
