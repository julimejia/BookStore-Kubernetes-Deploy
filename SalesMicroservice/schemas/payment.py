from pydantic import BaseModel

class PaymentCreate(BaseModel):
    purchase_id: int
    amount: float
    payment_method: str

class PaymentOut(BaseModel):
    id: int
    purchase_id: int
    amount: float
    payment_method: str
    payment_status: str

    class Config:
        orm_mode = True
