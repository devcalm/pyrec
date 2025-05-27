from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from app.models import Token
from app.deps import SessionDep
from typing import Annotated

from backend.app.services.auth import login

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Token)
async def login_route(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    return await login(session=session, email=form_data.username, password=form_data.password)  