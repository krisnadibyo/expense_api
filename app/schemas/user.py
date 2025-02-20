from pydantic import BaseModel

class UserCreate(BaseModel):
  username: str
  email: str
  password: str

class UserResponse(BaseModel):
  username: str
  email: str

class UserLogin(BaseModel):
  username: str
  password: str

class UserTokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"
