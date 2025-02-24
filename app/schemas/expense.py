from pydantic import BaseModel, validator
from datetime import date, datetime

class CategoryResponse(BaseModel):
  names: list[str] = []

class CategoryCreate(BaseModel):
  name: str

class CategoryCreateResponse(BaseModel):
  status: str = "OK"
  message: str = "A new category has been created"

class ExpenseResponse(BaseModel):
  id: int
  amount: int
  description: str
  date: str
  category_name: str

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
