from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, UserTokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException
from app.utils.string_utils import isemail
from app.schemas.user import UserUpdate

class UserService:
  def __init__(self, db: Session):
    self.db = db

  def create_user(self, user: UserCreate) -> UserResponse:
    # check if wa_number is not empty and valid number
    if not user.wa_number:
      raise HTTPException(status_code=400, detail="WhatsApp number is required")
    if user.wa_number and not user.wa_number.isdigit():
      raise HTTPException(status_code=400, detail="WhatsApp number must be a valid number")
    if not user.email:
      raise HTTPException(status_code=400, detail="Email is required")
    if user.email and not isemail(user.email):
      raise HTTPException(status_code=400, detail="Email must be a valid email")
    if not user.username:
      raise HTTPException(status_code=400, detail="Username is required")
    if not user.password:
      raise HTTPException(status_code=400, detail="Password is required")
    if len(user.password) < 4:
      raise HTTPException(status_code=400, detail="Password must be at least 4 characters long")

    # Check if email already exists
    if self.db.query(User).filter(User.email == user.email).first():
      raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if self.db.query(User).filter(User.username == user.username).first():
      raise HTTPException(status_code=400, detail="Username already registered")
    
    # Check if wa_number already exists
    if user.wa_number and self.db.query(User).filter(User.whatsapp_number == user.wa_number).first():
      raise HTTPException(status_code=400, detail="WhatsApp number already registered")
    
    # Create user
    db_user = User(
      email=user.email,
      username=user.username,
      hashed_password=get_password_hash(user.password),
      whatsapp_number=user.wa_number,
      is_active=True
    )

    # Add user to database
    self.db.add(db_user)
    self.db.commit()
    self.db.refresh(db_user)

    return UserResponse(
      username=db_user.username,
      email=db_user.email,
      wa_number=db_user.whatsapp_number
    )
  
  def update_user(self, user_id: int, user: UserUpdate) -> UserResponse:
    db_user = self.db.query(User).filter(User.id == user_id).first()
    if not db_user:
      raise HTTPException(status_code=404, detail="User not found")
  
    if user.wa_number:
      db_user.whatsapp_number = user.wa_number
    if user.username:
      db_user.username = user.username
    if user.email:
      db_user.email = user.email
    if user.password:
      db_user.hashed_password = get_password_hash(user.password)

    self.db.commit()
    self.db.refresh(db_user)
    
    return UserResponse(
      username=db_user.username,
      email=db_user.email,
      wa_number=db_user.whatsapp_number
    )

  def authenticate_user(self, user_login: UserLogin) -> UserTokenResponse:
    # find user by username
    user = self.db.query(User).filter(User.username == user_login.username).first()
    if not user:
      raise HTTPException(status_code=401, detail="Invalid username or password")
    
    # Check if password is correct
    if not verify_password(user_login.password, user.hashed_password):
      raise HTTPException(status_code=401, detail="Invalid username or password")
    
    #return access token
    access_token = create_access_token({
      "sub": str(user.id),
      "username": user.username,
      "email": user.email
      })
    
    # return user token response
    user_token_response = UserTokenResponse(
      access_token=access_token
    )
    return user_token_response

