from datetime import datetime, timedelta
from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseGet, ExpenseResponse, ExpensesResponse
from app.schemas.expense import ExpensePerCategoryResponse, ExpensesPerDayResponse

class ExpenseService:
  def __init__(self, db: Session):
    self.db = db

  def create_expense(self, expense_create: ExpenseCreate, user_id: int) -> ExpenseResponse:
    try:
      # Create new category by user
      new_row = Expense(
        amount= expense_create.amount,
        description= expense_create.description,
        date= expense_create.date,
        category_name= expense_create.category_name,
        user_id= user_id
      )

      # Add category to database
      self.db.add(new_row)
      self.db.commit()
      self.db.refresh(new_row)
      return ExpenseResponse(
        id= new_row.id,
        amount= new_row.amount,
        description= new_row.description,
        date= str(new_row.date),
        category_name= new_row.category_name
      )
    except SQLAlchemyError as e:
      self.db.rollback()
      raise HTTPException(
        status_code=400,
        detail=f"failed to create expense: {str(e)}"
      )   
  
  def get_expenses(self, expense_get: ExpenseGet, user_id: int) -> ExpensesResponse:
    try:
      expenses = self.db.query(Expense).filter(
        Expense.user_id == user_id,
        Expense.date >= expense_get.start_date,
        Expense.date <= expense_get.end_date
      ).order_by(Expense.date.desc()).limit(100).all()
      expenses_data = []
      total_sum = 0
      expenses_per_category = []
      expenses_per_day = []
      date_sums = {}
      category_sums = {}
      for expense in expenses:
        total_sum += expense.amount
        date_str = str(expense.date)
        expenses_data.append(ExpenseResponse(
          id= expense.id,
          amount= expense.amount,
          description= expense.description,
          date= date_str,
          category_name= expense.category_name
        ))
        if expense.category_name not in category_sums:
          category_sums[expense.category_name] = 0
        category_sums[expense.category_name] += expense.amount
        if date_str not in date_sums:
          date_sums[date_str] = 0
        date_sums[date_str] += expense.amount
      
      # Convert to list of ExpensePerCategoryResponse objects
      for category, amount in category_sums.items():
        expenses_per_category.append(ExpensePerCategoryResponse(
          category_name=category,
          amount=amount
        ))
      # Convert to list of ExpensesPerDayResponse objects
      for date, amount in date_sums.items():
        expenses_per_day.append(ExpensesPerDayResponse(
          date=date,
          amount=amount
        ))
      return ExpensesResponse(
        start_date= str(expense_get.start_date),
        end_date= str(expense_get.end_date),
        expenses= expenses_data,
        expenses_per_category= expenses_per_category,
        expenses_per_day= expenses_per_day,
        total_amount= total_sum
      )
    except SQLAlchemyError as e:
      raise HTTPException(status_code=500, detail=f"Failed to get expenses: {str(e)}")
    
  def get_expenses_range(self, range_type: str, user_id: int) -> ExpensesResponse:
    current_date = datetime.now().date()
    start_date = current_date
    end_date = current_date
    match range_type:
      case "today":
        pass
      case "week":
        start_date = current_date - timedelta(days=7)
        end_date = current_date
      case "month":
        start_date = current_date - timedelta(days=30)
        end_date = current_date
      case "quarter":
        start_date = current_date - timedelta(days=90)
        end_date = current_date
      case _:
        raise HTTPException(
          status_code=400,
          detail=f"Invalid range type: {range_type}. Must be one of: 'today', 'week', 'month', 'quarter'"
        )
    request = ExpenseGet(
      start_date= start_date,
      end_date= end_date
    )
    return self.get_expenses(request, user_id)
