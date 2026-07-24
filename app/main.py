from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlalchemy import text

from app.api.routes.auth import router as auth_router
from app.api.routes.users import router as users_router
from app.api.routes.categories import router as categories_router
from app.core.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
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

app.include_router(auth_router)
app.include_router(users_router)
app.include_router(categories_router)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a Ecommerce Backend API"
    }