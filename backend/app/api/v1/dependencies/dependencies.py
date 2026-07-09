from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_session
from app.repositories import CategoryRepository
from app.repositories.transaction import TransactionRepository
from app.services import CategoryService
from app.services.transaction_service import TransactionService


def get_category_repository(session: AsyncSession = Depends(get_session)) -> CategoryRepository:
    return CategoryRepository(session)

def get_category_service(repo: CategoryRepository = Depends(get_category_repository)) -> CategoryService:
    return CategoryService(repo)

def get_transaction_repository(session: AsyncSession = Depends(get_session)) -> TransactionRepository:
    return TransactionRepository(session)

def get_transaction_service(repo: TransactionRepository = Depends(get_transaction_repository)) -> TransactionService:
    return TransactionService(repo)