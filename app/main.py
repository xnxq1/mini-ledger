from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import merchant_router
from app.api.exceptions import register_exceptions
from app.infra.config import settings
from app.infra.db.connection import close_db
from app.infra.logging import get_logger, setup_logging

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application started")
    yield
    await close_db()
    logger.info("Application stopped")


def create_app() -> FastAPI:
    setup_logging(log_level=settings.log_level, json_logs=settings.json_logs)

    logger.info("Initializing application", version=settings.app_version)

    app = FastAPI(
        title=settings.app_name,
        description="Mini Ledger",
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
    )
    register_exceptions(app)
    app.include_router(merchant_router)

    @app.get("/")
    async def root():
        return {
            "status": "ok",
        }

    return app
