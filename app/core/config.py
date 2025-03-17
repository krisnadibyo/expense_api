from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
  model_config = {
      "env_file": ".env",
      "env_file_encoding": "utf-8"
  }
  DATABASE_URL: str = os.environ.get(
      "DATABASE_URL",
      "postgresql+psycopg2://postgres:postgres@localhost:5432/expense_tracker_v1"
  )
  SECRET_KEY: str = os.environ.get("SECRET_KEY")
  ALGORITHM: str = os.environ.get("ALGORITHM", "HS256")
  ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 1000))
  ACCESS_TOKEN_EXPIRE_DAYS: int = int(os.environ.get("ACCESS_TOKEN_EXPIRE_DAYS", 30))
settings = Settings() 