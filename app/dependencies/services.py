from fastapi import Depends
from app.db.session import get_db
from app.services.category_service import CategoryService
from app.services.expense_service import ExpenseService
from app.services.openai_service import OpenAIService
from app.services.user_service import UserService
from app.services.wa_service import WaService
from sqlalchemy.orm import Session

def get_openai_service() -> OpenAIService:
    return OpenAIService()

def get_wa_service(
    openai_service: OpenAIService = Depends(get_openai_service)
) -> WaService:
    return WaService(openai_service) 

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

def get_category_service(db: Session = Depends(get_db)) -> CategoryService:
    return CategoryService(db)

def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(db)

