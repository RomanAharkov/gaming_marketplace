from typing import Annotated
from fastapi import APIRouter, Body, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.user import User
from app.models.payment import Payment
from app.auth import require_admin
from app.schemas.payment import DepositRequest, DepositResponse, PaymentResponse
from app.services.payment import create_deposit


paymentRouter = APIRouter(prefix='/payments')


@paymentRouter.get('', status_code=200, response_model=list[PaymentResponse])
async def get_payments(session: Annotated[AsyncSession, Depends(get_db)],
                       _: Annotated[User, Depends(require_admin)]):
    result = await session.scalars(select(Payment))
    return result


@paymentRouter.post('/deposit', status_code=201, response_model=DepositResponse)
async def post_deposit(session: Annotated[AsyncSession, Depends(get_db)],
                       _: Annotated[User, Depends(require_admin)],
                       deposit_request: Annotated[DepositRequest, Body()]):

    await create_deposit(session, deposit_request)
    
    return DepositResponse(
        message = f"Successfully deposited {deposit_request.amount}$ into account with id {deposit_request.user_id}."
    )