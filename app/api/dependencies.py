from fastapi import Depends
from sqlalchemy.orm import Session
from app.services.category_service import CategoryService
from app.services.user_service import UserService
from app.db.session import get_db

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)