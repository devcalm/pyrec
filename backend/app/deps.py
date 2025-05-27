from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status
from app.core.db import engine
from app.core.config import settings
from app.services.security import ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import JWTError, jwt
from app.models import TokenPayload, User, UserRead
from sqlmodel.ext.asyncio.session import AsyncSession 
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncGenerator

async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl= "/auth/login"
)        

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep) -> UserRead:
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY,
            algorithms=[ALGORITHM], 
            audience=settings.AUDIENCE,
            issuer=settings.BASE_URL
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await session.get(User, token_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return UserRead(**user.model_dump())

CurrentUser = Annotated[UserRead, Depends(get_current_user)]


