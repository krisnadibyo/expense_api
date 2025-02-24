from sqlalchemy.orm import Session
from app.models import User
from app.schemas import UserCreate, UserLogin, UserResponse, UserTokenResponse
from app.core.security import get_password_hash, verify_password, create_access_token
from fastapi import HTTPException

class UserService:
  def __init__(self, db: Session):
    self.db = db

  def create_user(self, user: UserCreate) -> UserResponse:
    # Check if email already exists
    if self.db.query(User).filter(User.email == user.email).first():
      raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if username already exists
    if self.db.query(User).filter(User.username == user.username).first():
      raise HTTPException(status_code=400, detail="Username already registered")
    
    # Create user
    db_user = User(
      email=user.email,
      username=user.username,
      hashed_password=get_password_hash(user.password),
      is_active=True
    )

    # Add user to database
    self.db.add(db_user)
    self.db.commit()
    self.db.refresh(db_user)

    return UserResponse(
      username=db_user.username,
      email=db_user.email
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
