from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    book_id: int
    quantity: int
    

class PurchaseOut(BaseModel):
    id: int
    user_id: int
    book_id: int
    quantity: int
    total_price: float
    status: str
