from fastapi import FastAPI

from src.api.notebook.router import router as notebook_router


def create_app() -> FastAPI:
    """
    Creates and configures the FastAPI app.

    This function can be used to create the FastAPI app and include various routers,
    middlewares, and other configurations.

    Returns:
        FastAPI: The configured FastAPI application instance.
    """
    app = FastAPI(
        title="Notebook API",
        description="API for managing notebooks",
        version="1.0.0"
    )

    app.include_router(notebook_router, prefix="/notebooks", tags=["notebooks"])

    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
