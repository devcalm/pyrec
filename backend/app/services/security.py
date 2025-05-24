from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings
from app.models import Role, Token

ALGORITHM = "HS256"

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_tokens(*, sub: str, role: Role) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_TTL_MINUTES)
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_TTL_DAYS)

    access_token = create_token(
        data={"sub": sub, "role": role.value, "type": "access"},
        expires_delta=access_token_expires
    )
    refresh_token = create_token(
        data={"sub": sub, "type": "refresh"},
        expires_delta=refresh_token_expires
    )
    return Token(access_token=access_token, refresh_token=refresh_token)

def create_token(data: dict, expires_delta: timedelta) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)