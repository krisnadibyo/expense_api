from fastapi import APIRouter, Depends

from app.dependencies.services import get_category_service
from app.dependencies.auth import get_current_user
from app.services.category_service import CategoryService
from app.models import User
from app.schemas import CategoryCreate, CategoryCreateResponse, CategoryResponse

router = APIRouter(
  prefix="/categories",
  tags=["categories"]
)

@router.get("/", response_model=CategoryResponse)
async def get_categories(current_user: User = Depends(get_current_user), category_service: CategoryService =  Depends(get_category_service)):
  result = category_service.get_categories(user_id= current_user.id)
  return result

@router.post("/", response_model=CategoryCreateResponse)
async def get_categories(new_category: CategoryCreate, current_user: User = Depends(get_current_user), category_service: CategoryService =  Depends(get_category_service)):
  result = category_service.create_category(user_id= current_user.id, category_name=new_category.name)
  if result:
    return CategoryCreateResponse()
  else:
    return CategoryCreateResponse(success="Error", message= "error occured")
