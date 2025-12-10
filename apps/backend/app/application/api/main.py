# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI

import application
from application.api.healtcheck.handlers import router as healthcheck_router
from application.api.lifespan import close_message_broker, init_db, init_message_broker
from application.api.simulations.handlers import router as simulation_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: ARG001
    await init_db()
    await init_message_broker()

    yield

    await close_message_broker()


def create_app() -> "FastAPI":
    app = FastAPI(
        title="My API",
        version=application.__version__,
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
    app.include_router(healthcheck_router, prefix="/healthcheck")
    app.include_router(simulation_router, prefix="/simulation")

    return app
