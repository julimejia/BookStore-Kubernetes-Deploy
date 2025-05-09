from pydantic import BaseModel

class BookBase(BaseModel):
    title: str
    author: str
    description: str
    price: float
    stock: int

class BookCreate(BookBase):
    seller_id: int    

class BookOut(BookBase):
    id: int
    seller_id: int

    class Config:
        orm_mode = True
