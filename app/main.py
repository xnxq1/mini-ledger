from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI(
        title="Mini Ledger API",
        description="Система учета и управления финансами",
        version="0.1.0",
    )

    @app.get("/")
    async def root():
        return {
            "status": "ok",
        }

    return app
