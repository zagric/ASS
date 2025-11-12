# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

from application.api.lifespan import init_db
from application.api.simulations.handlers import router as simulation_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    await init_db()

    yield


def create_app() -> "FastAPI":
    app = FastAPI(
        title="My API",
        docs_url="/api/docs",
        redoc_url=None,
        description="API for My Application",
        license_info={
            "name": "MIT License",
            "identifier": "MIT",
        },
        lifespan=lifespan,
        debug=True,
    )
    app.include_router(simulation_router, prefix="/simulation")

    return app
