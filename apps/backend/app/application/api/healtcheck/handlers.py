# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#  Copyright (c) 2025 Aleksandr Zagrivnyy
# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
from fastapi import APIRouter
from starlette import status

from application.api.healtcheck.schemas import HealthCheckResponseSchema


router = APIRouter(tags=["Health Check"])


@router.get("", status_code=status.HTTP_200_OK, summary="Health Check")
def healthcheck_handler() -> HealthCheckResponseSchema:
    """Check server availability."""  # noqa: DOC201
    return HealthCheckResponseSchema()
