from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import CategoryModel
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: CategoryCreate) -> CategoryModel:
        category = CategoryModel(**data.model_dump())
        self.session.add(category)
        await self.session.flush()
        return category

    async def get_by_id(self, category_id: int) -> CategoryModel | None:
        result = await self.session.execute(
            select(CategoryModel).where(CategoryModel.id == category_id)
        )
        return result.scalar_one_or_none()

    async def list_all(self, include_archived: bool = False) -> list[CategoryModel]:
        query = select(CategoryModel).order_by(CategoryModel.sort_order, CategoryModel.id)
        if not include_archived:
            query = query.where(CategoryModel.is_archived.is_(False))
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def update(self, category_id: int, data: CategoryUpdate) -> CategoryModel | None:
        category = await self.get_by_id(category_id)
        if not category:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(category, key, value)

        return category

    async def delete(self, category_id: int) -> bool:
        category = await self.get_by_id(category_id)
        if not category:
            return False
        await self.session.delete(category)
        return True
