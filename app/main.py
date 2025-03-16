from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import users, auth, categories, expenses, whatsapp

app = FastAPI(
  title="Expense API Project",
  description="This is my api for my expense project",
  version="1.0.0",
  contact={
    "name": "Krisna D",
    "email": "krisnaatmojo@gmail.com",
  },
  # Disable automatic redirects for trailing slashes
  # This prevents FastAPI from redirecting /api/v1/categories to /api/v1/categories/
  redirect_slashes=False,
)

# Configure CORS with ngrok domain
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:8081",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8081",
    "https://polite-centrally-goat.ngrok-free.app",  # Your ngrok domain
    "http://polite-centrally-goat.ngrok-free.app",   # Both http and https versions
    # Add any other domains you need
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(expenses.router, prefix="/api/v1")
app.include_router(whatsapp.router, prefix="/whatsapp")
