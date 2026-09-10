from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.payment import DepositRequest
from app.models.payment import Payment, PaymentStatus, PaymentType
from app.models.user import User
from app.exceptions.user import UserNotFoundError

async def create_deposit(session: AsyncSession, deposit_request: DepositRequest):
    result = await session.execute(
        update(User)
        .where(
            User.id == deposit_request.user_id,
            User.is_deleted.is_(False)
        )
        .values(
            balance = User.balance + deposit_request.amount
        )
    )

    if result.rowcount == 0:
        raise UserNotFoundError('User not found.')

    payment = Payment(
        user_id = deposit_request.user_id,
        amount = deposit_request.amount,
        type = PaymentType.DEPOSIT,
        status = PaymentStatus.COMPLETED
    )

    session.add(payment)