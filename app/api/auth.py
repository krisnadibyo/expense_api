from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service
from app.schemas import UserCreate, UserLogin, UserResponse, UserTokenResponse
from app.services.user_service import UserService

router = APIRouter(
  prefix="/auth",
  tags=["auth"]
)

@router.post("/login", response_model=UserTokenResponse)
async def login(credentials: UserLogin, user_service: UserService = Depends(get_user_service)):
  return user_service.authenticate_user(credentials)

@router.post("/signup", response_model=UserResponse)
async def signup(user: UserCreate, user_service: UserService = Depends(get_user_service)):
  return user_service.create_user(user)

