from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.purchase import Purchase
from services.book_client import get_book, reduce_stock
from schemas.purchase import PurchaseCreate
from db import get_db

async def create_purchase_service(purchase: PurchaseCreate, user_id: int, db: Session = Depends(get_db)):
    # Obtener información del libro
    book = await get_book(purchase.book_id)
    
    # Verificar que haya suficiente stock
    if book["stock"] < purchase.quantity:
        raise HTTPException(status_code=400, detail="No hay suficiente stock disponible.")
    
    # Reducir el stock del libro
    await reduce_stock(purchase.book_id, purchase.quantity)
    
    # Calcular el total
    total_price = purchase.quantity * purchase.price

    # Crear la compra
    new_purchase = Purchase(
        user_id=user_id,
        book_id=purchase.book_id,
        quantity=purchase.quantity,
        total_price=total_price,
        status="Pending Payment"
    )

    # Guardar la compra en la base de datos
    db.add(new_purchase)
    db.commit()
    db.refresh(new_purchase)

    # Retornar la compra como respuesta
    return new_purchase
