from pydantic import BaseModel, field_validator, validator
from datetime import date, datetime

class ExpenseResponse(BaseModel):
  id: int
  amount: int
  description: str
  date: str
  category_name: str

class ExpenseDeleteResponse(BaseModel):
  status: str = "OK"
  message: str = "Expense deleted successfully"

class ExpenseGet(BaseModel):
  start_date: date
  end_date: date
  
  @field_validator('start_date', 'end_date', mode='before')
  @classmethod
  def parse_dates(cls, value):
    if isinstance(value, str):
      try:
          return datetime.strptime(value, "%Y-%m-%d").date()
      except ValueError:
          raise ValueError("Date must be in YYYY-MM-DD format")
    return value

class ExpensePerCategoryResponse(BaseModel):
  category_name: str
  amount: int

class ExpensesPerDayResponse(BaseModel):
  date: str
  amount: int

class ExpensesResponse(BaseModel):
  start_date: str
  end_date: str
  expenses: list[ExpenseResponse]
  expenses_per_category: list[ExpensePerCategoryResponse]
  expenses_per_day: list[ExpensesPerDayResponse]
  total_amount: int


class ExpensePerDayResponse(BaseModel):
  date: str
  total_amount: int

class ExpenseCreate(BaseModel):
  amount: int
  description: str
  date: date
  @validator('date', pre=True)
  def parse_date(cls, value):
    if isinstance(value, str):
      return datetime.strptime(value, "%Y-%m-%d").date()
    return value
  category_name: str

class ExpenseEdit(BaseModel):
  id: int
  amount: int | None = None
  description: str | None = None
  date: str | None = None
  category_name: str | None = None
