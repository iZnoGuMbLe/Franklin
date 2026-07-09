from datetime import date as date_type, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field

from app.models.transaction import CategorizationMethod, TransactionSource


class TransactionCreate(BaseModel):
    date: date_type
    amount: Decimal
    description: str = Field(..., min_length=1, max_length=500)
    currency: str = Field(default="RUB", max_length=3)
    category_id: int | None = None
    merchant_name: str | None = None
    is_income: bool = False
    comment: str | None = None
    source: TransactionSource = TransactionSource.MANUAL_ENTRY


class TransactionUpdate(BaseModel):
    date: date_type | None = None
    amount: Decimal | None = None
    description: str | None = Field(default=None, min_length=1, max_length=500)
    currency: str | None = None
    category_id: int | None = None
    merchant_name: str | None = None
    is_income: bool | None = None
    comment: str | None = None


class TransactionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date: date_type
    amount: Decimal
    currency: str
    description: str
    merchant_name: str | None
    category_id: int | None
    is_income: bool
    comment: str | None
    source: TransactionSource
    categorization_method: CategorizationMethod
    created_at: datetime
