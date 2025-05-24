from enum import StrEnum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    role: Role = Role.USER

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(SQLModel):
    email: str
    password: str

class Token(SQLModel):
    access_token: str
    refresh_token: str
