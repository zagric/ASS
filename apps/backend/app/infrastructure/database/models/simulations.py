# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from datetime import UTC, datetime

from sqlalchemy import Float, SmallInteger
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE
from sqlmodel import Field, SQLModel


class SimulationModel(SQLModel, table=True):
    __tablename__ = "simulations"

    id: int | None = Field(default=None, primary_key=True)
    oid: str = Field(index=True, unique=True)
    producers_count: int = Field(sa_type=SmallInteger, default=3)
    consumers_count: int = Field(sa_type=SmallInteger, default=3)
    buffer_size: int = Field(sa_type=SmallInteger, default=3)
    simulation_duration: int = Field(sa_type=SmallInteger, default=30)
    request_rate: float = Field(sa_type=Float, default=1)

    created_at: datetime = Field(
        default=datetime.now(tz=UTC),
        sa_type=DATETIME_TIMEZONE,
    )
