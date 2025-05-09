from sqlalchemy import Column, Integer, String, Float, Text
from db import Base  # Asegúrate de tener Base en tu archivo database.py

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(150), nullable=False)
    author = Column(String(100), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    seller_id = Column(Integer, nullable=False)  # Ya no es ForeignKey
