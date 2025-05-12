from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.purchase import Purchase
from services.book_client import get_book, reduce_stock
from schemas.purchase import PurchaseCreate
from db import get_db

async def create_purchase_service(token: str, purchase: PurchaseCreate, user_id: int, db: Session = Depends(get_db)):

    book = await get_book(purchase.book_id)
    price = book["price"]

    if book["stock"] < purchase.quantity:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")
  
    new_stock = book["stock"] - purchase.quantity
    await reduce_stock(purchase.book_id, new_stock, token)

    total_price = purchase.quantity * price

    new_purchase = Purchase(
        user_id=user_id,
        book_id=purchase.book_id,
        quantity=purchase.quantity,
        total_price=total_price,
        status="Pending Payment"
    )

    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    return new_purchase
