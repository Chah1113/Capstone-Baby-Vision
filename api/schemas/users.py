from pydantic import BaseModel, EmailStr, Field

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshRequest(BaseModel):
    refresh_token: str

class UserProfileUpdate(BaseModel):
    name: str = Field(min_length=1, max_length=100)

class UserPasswordUpdate(BaseModel):
    current_password: str
    new_password: str = Field(min_length=8)

class UserDeleteRequest(BaseModel):
    password: str
