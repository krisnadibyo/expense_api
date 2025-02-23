from fastapi import FastAPI
from .api import users, auth, categories

app = FastAPI(
  title="Expense API Project",
  description="This is my api for my expense project",
  version="1.0.0",
  contact={
    "name": "Krisna D",
    "email": "krisnaatmojo@gmail.com",
  },
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")


