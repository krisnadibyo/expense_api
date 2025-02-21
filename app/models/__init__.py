from app.models.base import Base
# Import all your models here
from app.models.user import User

# List all models for easy import
__all__ = ["User", "Base"]
