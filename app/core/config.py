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
    
settings = Settings() 