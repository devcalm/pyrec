from enum import StrEnum
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone

class Role(StrEnum):
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    role: Role = Role.USER
    hashed_password: str

class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

class UserCreate(SQLModel):
    email: str
    password: str
 
class UserRead(UserBase):
    id: int

class File(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    owner_id: int = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Token(SQLModel):
    access_token: str
    refresh_token: str

class TokenPayload(SQLModel):
    sub: str | None = None
    id: int | None = None
