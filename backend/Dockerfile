FROM python:3.13-slim-bookworm AS base
COPY --from=ghcr.io/astral-sh/uv:0.8.21 /uv /uvx /bin/

WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy


FROM base AS dev
ENV PATH="/app/.venv/bin:$PATH"

COPY uv.lock pyproject.toml . ./
RUN uv sync

EXPOSE 8000 5678
ENTRYPOINT ["uvicorn", "--factory", "application.api.main:create_app", "--timeout-graceful-shutdown", "2", "--host", "0.0.0.0", "--port", "8000", "--reload"]


FROM base AS builder
COPY uv.lock pyproject.toml ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-default-groups

COPY app/ ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-default-groups


FROM python:3.13-slim-bookworm AS runtime
ENV PATH="/app/.venv/bin:$PATH"

RUN groupadd -g 1001 appgroup && \
    useradd -u 1001 -g appgroup -m  -d /app -s /bin/false appuser

WORKDIR /app

COPY --from=builder --chown=appuser:appgroup /app ./

USER appuser

EXPOSE 8000

ENTRYPOINT ["uvicorn", "--factory", "application.api.main:create_app", "--host", "0.0.0.0", "--port", "8000"]
