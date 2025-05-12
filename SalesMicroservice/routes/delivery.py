from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import get_db
from models.delivery import DeliveryProvider
from models.delivery_assignment import DeliveryAssignment
from schemas.delivery import DeliveryProviderOut
from schemas.delivery_ass import DeliveryAssignmentCreate
from typing import List

router = APIRouter()

@router.get("/", response_model=List[DeliveryProviderOut])
def get_providers(db: Session = Depends(get_db)):
    providers = db.query(DeliveryProvider).all()
    return providers

@router.post("/assign")
def assign_provider(assignment: DeliveryAssignmentCreate, db: Session = Depends(get_db)):
    new_assignment = DeliveryAssignment(**assignment.dict())
    db.add(new_assignment)
    db.commit()
    db.refresh(new_assignment)
    return {"message": "Provider assigned successfully", "assignment_id": new_assignment.id}
