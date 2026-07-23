from fastapi import FastAPI

app = FastAPI(
    title="Ecommerce Backend API",
    description="Backend profesional desarrollado con FastAPI",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "Bienvenido a Ecommerce Backend API"
    }