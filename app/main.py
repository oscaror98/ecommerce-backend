from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown events.
    """

    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))

        print("Database connection established successfully.")

    except Exception as error:
        print(f"Database connection failed: {error}")
        raise

    yield


app = FastAPI(
    title="Ecommerce Backend API",
    description="Backend profesional desarrollado con FastAPI",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a Ecommerce Backend API"
    }