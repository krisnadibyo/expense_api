from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password) -> str:
  return pwd_context.hash(password)

def create_access_token(data: dict) -> str:
  to_encode = data.copy()
  expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
  return encoded_jwt

def create_whatsapp_auth_key(wa_number: str) -> str:
    to_encode = {"sub": wa_number}
    expire = datetime.now(timezone.utc) + timedelta(days=settings.ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "whatsapp"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
  