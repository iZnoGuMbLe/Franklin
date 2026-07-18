from fastapi import Depends, APIRouter, status
from datetime import date
from decimal import Decimal

from app.schemas.transaction import TransactionResponse,TransactionUpdate,TransactionCreate
from app.services.transaction_service import TransactionService
from app.api.v1.dependencies import get_transaction_service

router = APIRouter(prefix='/transactions', tags=['transactions'])


@router.post(response_model=TransactionResponse, path='', status_code=status.HTTP_201_CREATED)
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

    return response


@router.patch(response_model=TransactionResponse,path='/{transaction_id}', status_code=status.HTTP_200_OK)
async def update_transaction(
        transaction_id: int,
        data: TransactionUpdate,
        service: TransactionService = Depends(get_transaction_service)
) -> TransactionResponse:

    response = await service.update_transaction(transaction_id=transaction_id, data=data)

    return response

@router.get(response_model=list[TransactionResponse], path='')
async def get_list_of_transaction(date_from: date | None = None,
                               date_to: date | None = None,
                               category_id: int | None = None,
                               is_income: bool | None = None,
                               min_amount: Decimal | None = None,
                               max_amount: Decimal | None = None,
        service: TransactionService = Depends(get_transaction_service)
)-> list[TransactionResponse]:
    return await service.list_of_transactions(date_from=date_from, date_to=date_to, category_id=category_id, is_income=is_income, min_amount=min_amount,max_amount=max_amount)

@router.delete(path='/{transaction_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
        transaction_id: int,
        service: TransactionService = Depends(get_transaction_service)
):
    await service.delete_transaction(transaction_id=transaction_id)


