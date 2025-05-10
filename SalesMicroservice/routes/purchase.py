from fastapi import APIRouter, Depends
from schemas.purchase import PurchaseCreate, PurchaseOut
from utils.jwt import get_current_user_id
from services.purchase_service import create_purchase_service
from db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/purchase", response_model=PurchaseOut)
async def create_purchase(
    purchase: PurchaseCreate,
    user_id: int = Depends(get_current_user_id),  # Obtener el user_id como dependencia
    db: Session = Depends(get_db)                 # Obtener la sesión de base de datos
):
    new_purchase = await create_purchase_service(purchase, user_id, db)
    return new_purchase
