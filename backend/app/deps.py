from collections.abc import Generator
from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from app.core.db import engine
from app.core.config import settings
from app.services.security import ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from pydantic import ValidationError
from jose import JWTError, jwt
from app.models import TokenPayload, User

def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl= "/auth/login"
)        

SessionDep = Annotated[Session, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

def get_current_user(session: SessionDep, token: TokenDep) -> User:
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
    user = session.get(User, token_data.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]


