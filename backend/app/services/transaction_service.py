from app.schemas.transaction import TransactionResponse, TransactionUpdate, TransactionCreate
from app.repositories.transaction import TransactionRepository


class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository


    async def create_transaction(self, data:TransactionCreate) -> TransactionResponse | None:
        transaction = await self.repository.create(data=data)
        return TransactionResponse.model_validate(transaction)


    async def get_transaction(self,transaction_id: int) -> TransactionResponse | None:
        transaction = await self.repository.get_by_id(transaction_id=transaction_id)
        if not transaction:
            return None
        return TransactionResponse.model_validate(transaction)



    async def update_transaction(self,transaction_id: int, data: TransactionUpdate ) -> TransactionResponse | None:
        updated_transaction = await self.repository.update(
            transaction_id=transaction_id, data=data)
        if not updated_transaction:
            return None
        return TransactionResponse.model_validate(updated_transaction)


    async def list_of_transactions(self) -> list[TransactionResponse]:
        result = await self.repository.list_of_transactions()
        return [TransactionResponse.model_validate(x) for x in result]



    async def delete_transaction(self, transaction_id) -> bool:
        return await self.repository.delete(transaction_id=transaction_id)
