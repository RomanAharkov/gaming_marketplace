from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import User
from app.auth import get_current_user, require_admin
from app.database import get_db
from app.schemas.user import UserResponse


userRouter = APIRouter()

@userRouter.get('/users', response_model=list[UserResponse])
async def get_users(_: Annotated[User, Depends(require_admin)],
                    session: Annotated[AsyncSession, Depends(get_db)]):
    users = await session.scalars(select(User))
    return users.all()