from pydantic import BaseModel

class CategoryResponse(BaseModel):
  id: int
  name: str

class ExpenseResponse(BaseModel):
  id: int
  amount: int
  description: str
  date: str
  category: CategoryResponse

class ExpenseCreate(BaseModel):
  amount: int
  description: str
  date: str
  category_id: int

class CreateCategory(BaseModel):
  name: str

