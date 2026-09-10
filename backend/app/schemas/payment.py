from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field
from app.models.payment import PaymentType, PaymentStatus


class DepositRequest(BaseModel):
    user_id: int = Field(gt=0)
    amount: Decimal = Field(gt=0, decimal_places=2)

class DepositResponse(BaseModel):
    message: str

class PaymentResponse(BaseModel):
    id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    order_id: int | None = Field(default=None, gt=0)
    amount: Decimal = Field(decimal_places=2, gt=0)
    type: PaymentType
    status: PaymentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)