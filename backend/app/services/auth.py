from sqlmodel import Session, select

from app.models import Token, User
from app.services.security import create_tokens, verify_password
from fastapi import HTTPException, status

def get_user_by_email(*, session: Session, email: str) -> User | None:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def authenticate(*, session: Session, email: str, password: str) -> User | None:
    user = get_user_by_email(session=session, email=email)
    if not user:
        return None   
    if not verify_password(password, user.hashed_password):
        return None
    return user

def login(*, session: Session, email: str, password: str) -> Token:
    user = authenticate(session=session, email=email, password=password)
    if not user:
        raise unauthorized_exception("Incorrect email or password")
    elif not user.is_active:
        raise unauthorized_exception("Inactive user")
    return create_tokens(user)

def unauthorized_exception(detail: str) -> HTTPException: 
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail,
        headers={"WWW-Authenticate": "Bearer"}
    )


