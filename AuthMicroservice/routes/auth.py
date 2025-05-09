from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from schemas.user import UserCreate, UserLogin, Token
from db import get_db
from utils.auth_utils import hash_password, verify_password, create_access_token

auth_router = APIRouter()

@auth_router.post("/register", status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hash_password(user_data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@auth_router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if not user or not verify_password(credentials.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": token}

@auth_router.post("/logout")
def logout():
    # En JWT no se hace logout server-side, el cliente solo elimina el token.
    return {"message": "Logout successful. Discard your token on the client."}
