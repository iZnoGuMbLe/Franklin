from app.schemas.transaction import TransactionResponse, TransactionUpdate, TransactionCreate
from app.repositories.transaction import TransactionRepository
from app.core import NotFoundException

class TransactionService:

    def __init__(self, repository: TransactionRepository):
        self.repository = repository


    async def create_transaction(self, data:TransactionCreate) -> TransactionResponse:
        transaction = await self.repository.create(data=data)
        return TransactionResponse.model_validate(transaction)


    async def get_transaction(self,transaction_id: int) -> TransactionResponse:
        transaction = await self.repository.get_by_id(transaction_id=transaction_id)
        if not transaction:
            raise NotFoundException(entity="Transaction", entity_id=transaction_id)
        return TransactionResponse.model_validate(transaction)



    async def update_transaction(self,transaction_id: int, data: TransactionUpdate ) -> TransactionResponse:
        updated_transaction = await self.repository.update(
            transaction_id=transaction_id, data=data)
        if not updated_transaction:
            raise NotFoundException(entity="Transaction", entity_id=transaction_id)
        return TransactionResponse.model_validate(updated_transaction)


    async def list_of_transactions(self) -> list[TransactionResponse]:
        result = await self.repository.list_of_transactions()
        return [TransactionResponse.model_validate(x) for x in result]



    async def delete_transaction(self, transaction_id) -> bool:
        transaction = await self.repository.get_by_id(transaction_id=transaction_id)
        if not transaction:
            raise NotFoundException(entity="Transaction", entity_id=transaction_id)
        return await self.repository.delete(transaction_id=transaction_id)
