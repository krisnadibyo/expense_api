from fastapi import APIRouter, Depends

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(
  prefix="/users",
  tags=["users"]
)

@router.get("/me", response_model=UserResponse)
async def get_users_me(current_user: User = Depends(get_current_user)):
  user_response = UserResponse(
    username=current_user.username,
    email=current_user.email
  )
  return user_response
