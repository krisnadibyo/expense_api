from asyncio.log import logger
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.db.session import get_db
from app.models.user import User
from sqlalchemy.orm import Session
from app.core.config import settings
from jose import jwt, JWTError

# This means the token endpoint will be at /api/auth/login
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
  #define credentials exception
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
  )
  #decode jwt token
  try:
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    print("payload", payload)
    user_id = payload.get("sub")
    print("user_id", user_id)
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
      raise credentials_exception
    return user
  except JWTError as e:
    print("JWTError", e)
    raise credentials_exception
