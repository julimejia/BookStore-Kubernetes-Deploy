from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Purchase(Base):
    __tablename__ = 'purchases'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    book_id = Column(Integer)
    quantity = Column(Integer)
    total_price = Column(Float)
    status = Column(String, default='Pending Payment')
