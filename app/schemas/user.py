from pydantic import BaseModel

class UserCreate(BaseModel):
  username: str
  email: str
  password: str
  wa_number: str = None

class UserUpdate(BaseModel):
  wa_number: str = None
  username: str = None
  email: str = None
  password: str = None

class UserResponse(BaseModel):
  username: str
  email: str
  wa_number: str

class UserLogin(BaseModel):
  username: str
  password: str

class UserTokenResponse(BaseModel):
  access_token: str
  token_type: str = "bearer"
