from pydantic import BaseModel

class DeliveryAssignmentCreate(BaseModel):
    purchase_id: int
    provider_id: int
