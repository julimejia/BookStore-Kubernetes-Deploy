from fastapi import FastAPI
from routes import purchase, payment,delivery

app = FastAPI(title="Sales Service")

app.include_router(purchase.router, prefix="/purchase", tags=["Purchase"])
app.include_router(payment.router, prefix="/payment", tags=["Payment"])
app.include_router(delivery.router, prefix="/delivery", tags=["Delivery"])