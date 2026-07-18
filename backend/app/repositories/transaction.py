import hashlib
from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

from app.models.transaction import TransactionModel
from app.schemas.transaction import TransactionCreate,TransactionUpdate

class TransactionRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TransactionCreate) -> TransactionModel:

        payload = data.model_dump()
        raw = f'{data.date} | {data.amount} | {data.description} | {data.merchant_name}'
        payload["dedup_hash"] = hashlib.sha256(raw.encode()).hexdigest()
        transaction = TransactionModel(**payload)
        self.session.add(transaction)
        await self.session.flush()
        return transaction


    async def get_by_id(self, transaction_id: int) -> TransactionModel | None:
        result = await self.session.execute(select(TransactionModel).where(TransactionModel.id == transaction_id))

        return result.scalar_one_or_none()

    async def list_of_transactions(self,
                date_from: date | None = None,
                date_to: date | None = None,
                category_id: int | None = None,
                is_income: bool | None = None,
                min_amount: Decimal | None = None,
                max_amount: Decimal | None = None
            ) -> list[TransactionModel]:


        query = select(TransactionModel)
        if date_from is not None:
            query = query.where(TransactionModel.date >= date_from)
        if date_to is not None:
            query = query.where(TransactionModel.date <= date_to)
        if category_id is not None:
            query = query.where(TransactionModel.category_id == category_id)
        if is_income is not None:
            query = query.where(TransactionModel.is_income == is_income)
        if min_amount is not None:
            query = query.where(TransactionModel.amount >= min_amount)
        if max_amount is not None:
            query = query.where(TransactionModel.amount <= max_amount)

        query = query.order_by(desc(TransactionModel.date), desc(TransactionModel.id))
        result = await self.session.execute(query)

        return list(result.scalars().all())


    async def update(self, transaction_id: int, data: TransactionUpdate) -> TransactionModel | None:
        transaction = await self.get_by_id(transaction_id)

        if not transaction:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(transaction, key, value)

        return transaction


    async def delete(self, transaction_id: int) -> bool:

        transaction = await self.get_by_id(transaction_id)

        if not transaction:
            return False
        await self.session.delete(transaction)
        return True


