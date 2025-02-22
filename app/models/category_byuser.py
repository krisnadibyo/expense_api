from sqlalchemy import Column, ForeignKey, Integer, String
from app.models.base import Base


class CategoryByUser(Base):
  __tablename__ = "categories_byuser"
  id = Column(Integer, primary_key=True)
  name = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), index=True)
