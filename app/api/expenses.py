from fastapi import APIRouter, Depends

from app.api.dependencies import get_expense_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.services.expense_service import ExpenseService

router = APIRouter(
  prefix="/expenses",
  tags=["expenses"]
)

@router.post("/", response_model=ExpenseResponse)
async def create_expense(expense_create: ExpenseCreate, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.create_expense(expense_create=expense_create, user_id=current_user.id)
  return result
