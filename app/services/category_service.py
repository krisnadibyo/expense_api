from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models.category import Category
from app.models.category_byuser import CategoryByUser
from app.schemas.expense import CategoryResponse

class CategoryService:
  def __init__(self, db: Session):
    self.db = db

  def get_categories(self, user_id: int) -> CategoryResponse:
      categories_default = self.db.query(Category)
      if not categories_default:
         raise HTTPException(status_code=404, detail="Categories are not found")
      result = CategoryResponse()
      for category in categories_default:
         result.names.append(category.name)
      categories_byuser = self.db.query(CategoryByUser).filter(CategoryByUser.user_id == user_id)
      if not categories_byuser:
         return result
      for category_byuser in categories_byuser:
         result.names.append(category_byuser.name)
      return result
  def create_category(self, user_id: int, category_name: str) -> bool:
    try:
      # Create new category by user
      new_row = CategoryByUser(
        name=category_name,
        user_id=user_id
      )

      # Add category to database
      self.db.add(new_row)
      self.db.commit()
      self.db.refresh(new_row)

      #verify the row was created by check
      if new_row.id:
         return True
      return False
    except SQLAlchemyError as e:
       self.db.rollback()
       raise HTTPException(
          status_code=400,
          detail=f"failed to create category: {str(e)}"
       )     
