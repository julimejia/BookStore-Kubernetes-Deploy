from sqlalchemy.orm import Session
from schemas.payment import PaymentCreate
from models.payment import Payment
from models.purchase import Purchase


def create_payment_and_update_purchase(db: Session, data: PaymentCreate):

    payment = Payment(
        purchase_id=data.purchase_id,
        amount=data.amount,
        payment_method=data.payment_method,
        payment_status="Paid"
    )
    db.add(payment)

    purchase = db.query(Purchase).get(data.purchase_id)
    if not purchase:
        raise Exception("Purchase not found")
    purchase.status = "Paid"

    db.commit()
    db.refresh(payment)
    return payment
