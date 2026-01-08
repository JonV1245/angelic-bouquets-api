from fastapi import FastAPI
from app.routers.customers import router as customers_router

app = FastAPI(
    title="Angelic Bouquets API",
    version="0.1.0",
    description="Backend API for managing customers and orders for Angelic Bouquets."
)

@app.get("/health", tags=["system"])
def health():
    return {"status": "ok"}

app.include_router(customers_router)