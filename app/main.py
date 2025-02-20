from fastapi import FastAPI
from .api import users

app = FastAPI(
  title="My Api",
  description="This is my api for my expense project",
  version="1.0.0",
  contact={
    "name": "Krisna D",
    "email": "krisnaatmojo@gmail.com",
  },
)

app.include_router(users.router, prefix="/api/v1")

@app.get("/hello")
async def root():
  return {"message": "Hello World"}

