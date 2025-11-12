# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    pg_connection_uri: str = Field(alias="PG_CONNECTION_URI")
