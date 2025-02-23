from sqlalchemy import Column, Date, ForeignKey, Integer, String

from app.models.base import Base


class Expense(Base):
  __tablename__ = "expenses"
  id = Column(Integer, primary_key=True)
  amount = Column(Integer, nullable=False)
  description = Column(String, nullable=False)
  date = Column(Date, nullable=False)
  category_name = Column(String, nullable=False)
  user_id = Column(Integer, ForeignKey("users.id"), index=True)