from sqlalchemy import Column, Integer, String, Float
from db import Base

class DeliveryProvider(Base):
    __tablename__ = "delivery_providers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    coverage_area = Column(String(150), nullable=False)
    cost = Column(Float, nullable=False)
