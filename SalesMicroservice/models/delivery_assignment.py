from sqlalchemy import Column, Integer, ForeignKey
from db import Base
from models.purchase import Purchase
from models.delivery import DeliveryProvider

class DeliveryAssignment(Base):
    __tablename__ = "delivery_assignments"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey(Purchase.id), nullable=False)
    provider_id = Column(Integer, ForeignKey(DeliveryProvider.id), nullable=False)
