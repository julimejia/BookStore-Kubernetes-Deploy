from fastapi import FastAPI
from routes import purchase

app = FastAPI(title="Purchase Service")

app.include_router(purchase.router, prefix="/purchase", tags=["Purchase"])