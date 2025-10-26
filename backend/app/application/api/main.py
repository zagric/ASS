from fastapi import FastAPI


def create_app() -> "FastAPI":
    return FastAPI(
        title="My API",
        docs_url="/api/docs",
        description="API for My Application",
        debug=True
    )