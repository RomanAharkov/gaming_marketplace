from app.database import get_db
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
from app.schemas.user import UserCreate


authRouter = APIRouter()

@authRouter.post('/register')
async def register(session: Annotated[Session, Depends(get_db)],
                   user_data: Annotated[UserCreate, Body()]):
    pass

@authRouter.post('/login')
async def login(session: Annotated[Session, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass