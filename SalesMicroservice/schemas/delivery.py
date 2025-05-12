from pydantic import BaseModel

class DeliveryProviderOut(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
