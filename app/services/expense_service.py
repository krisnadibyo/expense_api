from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import Expense
from app.schemas import ExpenseCreate, ExpenseGet, ExpenseResponse, ExpensesResponse

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
      ).all()
      expenses_response = [ExpenseResponse(
        id= expense.id,
        amount= expense.amount,
        description= expense.description,
        date= str(expense.date),
        category_name= expense.category_name
      ) for expense in expenses]
      return ExpensesResponse(
        start_date= str(expense_get.start_date),
        end_date= str(expense_get.end_date),
        expenses= expenses_response,
        total_amount= sum(expense.amount for expense in expenses)
      )
    except SQLAlchemyError as e:
      raise HTTPException(status_code=500, detail=f"Failed to get expenses: {str(e)}")