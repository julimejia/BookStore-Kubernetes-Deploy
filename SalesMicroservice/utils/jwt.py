from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # tokenUrl no se usa aquí pero es requerido

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

class TokenData(BaseModel):
    user_id: int

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        print("Este es el user id mi brokoli", user_id)
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido: user_id faltante")
        return user_id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )
