from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import users, auth, categories,expenses, whatsapp

app = FastAPI(
  title="Expense API Project",
  description="This is my api for my expense project",
  version="1.0.0",
  contact={
    "name": "Krisna D",
    "email": "krisnaatmojo@gmail.com",
  },
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",    # For React default port
    "http://localhost:8081",    # For FastAPI default port
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8081",
    # Add any other origins (frontend URLs) you want to allow
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],        # Allows all methods
    allow_headers=["*"],        # Allows all headers
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(expenses.router, prefix="/api/v1")
app.include_router(whatsapp.router, prefix="/whatsapp")
