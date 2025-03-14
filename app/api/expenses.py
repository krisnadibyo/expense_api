from datetime import datetime
from fastapi import APIRouter, Depends, Path

from app.dependencies.services import get_expense_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseGet, ExpenseResponse, ExpensesResponse
from app.services.expense_service import ExpenseService

router = APIRouter(
  prefix="/expenses",
  tags=["expenses"]
)

@router.post("/", response_model=ExpenseResponse)
async def create_expense(expense_create: ExpenseCreate, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.create_expense(expense_create=expense_create, user_id=current_user.id)
  return result

@router.get("/", response_model=ExpensesResponse)
async def get_expenses(expense_get: ExpenseGet, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.get_expenses(expense_get=expense_get, user_id=current_user.id)
  return result

@router.get("/{range_type}", response_model=ExpensesResponse)
async def get_expenses_range(
  range_type: str = Path(..., description="The type of range: 'today','week','month','quarter'"),
  current_user: User = Depends(get_current_user), 
  expense_service: ExpenseService = Depends(get_expense_service)
):
  result = expense_service.get_expenses_range(range_type=range_type, user_id=current_user.id)
  return result