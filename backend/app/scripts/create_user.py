import sys
import asyncio
import getpass
from pydantic import BaseModel, EmailStr, ValidationError
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession 
from app.core.db import engine
from app.models import User, Role
from app.deps import async_session
from app.services.security import hash_password

class EmailCheck(BaseModel):
    email: EmailStr

async def main():
    email_input:str = input("Enter email: ").strip()
    try:
        email_check = EmailCheck(email=email_input) 
    except ValidationError as e:
        print("❌ Invalid email format:", e)
        sys.exit(1)

    print(f"Available roles: {[r.value for r in Role]}")
    role_input:str = input("Enter role: ").lower()
    try:
        role = Role(role_input)
    except ValueError:
        print(f"❌ Invalid role '{role_input}'. Must be one of: {[r.value for r in Role]}")
        exit(1)     

    password:str = getpass.getpass("Enter password: ")
    if not password:
        print("❌ Password must not be empty.")
        sys.exit(1)

    password_confirm:str = getpass.getpass("Confirm password: ")
    if not password_confirm:
        print("❌ Confirm password must not be empty.")
        sys.exit(1)

    if (password != password_confirm):
        print("❌ Passwords do not match.")
        sys.exit(1)

    async with async_session() as session:
        result = await session.exec(select(User).where(User.email == email_check.email))
        user_exists = result.first()

        if user_exists:
            print("❌ User with this email already exists.")
            sys.exit(1)

        new_user = User(
            email=email_input,
            hashed_password=hash_password(password),
            is_active=True,
            role=role,
        )

        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)

        print(f"✅ User created with ID {new_user.id}")     

if __name__ == "__main__":
   asyncio.run(main())     