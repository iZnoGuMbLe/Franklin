from fastapi import Depends, APIRouter, HTTPException, status

from app.schemas.transaction import TransactionResponse,TransactionUpdate,TransactionCreate
from app.services.transaction_service import TransactionService
from app.api.v1.dependencies import get_transaction_service

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post(response_model=TransactionResponse, path='')
async def create_transaction(
        data: TransactionCreate,
        service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:
    return await service.create_transaction(data=data)


@router.get(response_model=TransactionResponse, path='/{transaction_id}')
async def get_transaction(
        transaction_id:int,
        service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:

    response = await service.get_transaction(transaction_id=transaction_id)
    if response is None:
        raise HTTPException(status_code=404, detail='Transaction not found')

    return response


@router.patch(response_model=TransactionResponse,path='/{transaction_id}')
async def update_transaction(
        transaction_id: int,
        data: TransactionUpdate,
        service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:

    response = await service.update_transaction(transaction_id=transaction_id, data=data)
    if response is None:
        raise HTTPException(status_code=404, detail='Transaction not found')

    return response

@router.get(response_model=list[TransactionResponse], path='')
async def get_list_of_transaction(
        service: TransactionService = Depends(get_transaction_service)
)-> list[TransactionResponse]:
    return await service.list_of_transactions()

@router.delete(path='/{transaction_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
        transaction_id: int,
        service: TransactionService = Depends(get_transaction_service)
):
    response = await service.delete_transaction(transaction_id=transaction_id)
    if not response:
        raise HTTPException(status_code=404, detail='Transaction not found')

    return None
