from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.purchase import Purchase

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    purchase_id = Column(Integer, ForeignKey(Purchase.id))
    amount = Column(Float)
    payment_method = Column(String)
    payment_status = Column(String)
