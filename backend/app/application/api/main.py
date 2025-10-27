# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from fastapi import FastAPI

from application.api.simulations.handlers import router as simulation_router


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
        debug=True,
    )
    app.include_router(simulation_router, prefix="/simulation")

    return app
