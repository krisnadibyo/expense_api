from pydantic import BaseModel

class CategoryResponse(BaseModel):
  names: list[str] = []

class CategoryCreate(BaseModel):
  name: str

class CategoryEdit(BaseModel):
  name: str
  new_name: str

class CategoryDelete(BaseModel):
  name: str

class CategoryDeleteResponse(BaseModel):
  status: str = "OK"
  message: str = "A new category has been deleted"

class CategoryCreateResponse(BaseModel):
  status: str = "OK"
  message: str = "A new category has been created"

class CategoryEditResponse(BaseModel):
  status: str = "OK"
  message: str = "A new category has been Edited"