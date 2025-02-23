from pydantic import BaseModel

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
  category: CategoryResponse

class ExpenseCreate(BaseModel):
  amount: int
  description: str
  date: str
  category_id: int

class CreateCategory(BaseModel):
  name: str

