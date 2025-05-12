from fastapi import APIRouter, Depends
from utils.jwt import get_current_user_id
from db import get_db
from sqlalchemy.orm import Session
from utils.jwt import get_current_user_id, oauth2_scheme
from schemas.payment import PaymentCreate, PaymentOut
from services.payment_service import create_payment_and_update_purchase




router = APIRouter()
@router.post("/payments/", response_model=PaymentOut)
def make_payment(payment: PaymentCreate, db: Session = Depends(get_db)):
    return create_payment_and_update_purchase(db, payment)