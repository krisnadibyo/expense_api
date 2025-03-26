from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, Path

from app.dependencies.services import get_expense_service
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.schemas.expense import ExpenseCreate, ExpenseDeleteResponse, ExpenseEdit, ExpenseGet, ExpenseResponse, ExpensesResponse
from app.services.expense_service import ExpenseService

router = APIRouter(
  prefix="/expenses",
  tags=["expenses"]
)

@router.post("", response_model=ExpenseResponse)
async def create_expense(expense_create: ExpenseCreate, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.create_expense(expense_create=expense_create, user_id=current_user.id)
  return result

@router.get("", response_model=ExpensesResponse)
async def get_expenses(start_date: Optional[str] = None, end_date: Optional[str] = None, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.get_expenses(start_date=start_date, end_date=end_date, user_id=current_user.id)
  return result

@router.put("", response_model=ExpenseResponse)
async def edit_expense(expense_edit: ExpenseEdit, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.edit_expense(expense_edit=expense_edit, user_id=current_user.id)
  return result

@router.delete("/{expense_id}", response_model=ExpenseDeleteResponse)
async def delete_expense(expense_id: int, current_user: User = Depends(get_current_user), expense_service: ExpenseService = Depends(get_expense_service)):
  result = expense_service.delete_expense(expense_id=expense_id, user_id=current_user.id)
  if result:
    return ExpenseDeleteResponse()
  else:
    return ExpenseDeleteResponse(success="Error", message= "Error deleting expense")

@router.get("/{range_type}", response_model=ExpensesResponse)
async def get_expenses_range(
  range_type: str = Path(..., description="The type of range: 'today','week','month','quarter'"),
  current_user: User = Depends(get_current_user), 
  expense_service: ExpenseService = Depends(get_expense_service)
):
  print(f"Getting expenses range for user {current_user.id} with range type {range_type}")
  result = expense_service.get_expenses_range(range_type=range_type, user_id=current_user.id)
  return result