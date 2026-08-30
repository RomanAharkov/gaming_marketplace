from app.database import get_db
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated


authRouter = APIRouter()

@authRouter.post('/register')
async def register(session: Annotated[Session, Depends(get_db)]):
    pass

@authRouter.post('/login')
async def login(session: Annotated[Session, Depends(get_db)],
                form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    pass