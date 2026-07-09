
from app.repositories.category import CategoryRepository
from app.schemas import CategoryResponse, CategoryUpdate, CategoryCreate



class CategoryService:

    def __init__(self, repository: CategoryRepository):
        self.repository = repository

    async def create_category(self, data: CategoryCreate) -> CategoryResponse:
        categorya = await self.repository.create(data)
        return CategoryResponse.model_validate(categorya)


    async def get_category(self, category_id: int) -> CategoryResponse | None:
        categorya = await self.repository.get_by_id(category_id)
        if not categorya:
            return None
        return CategoryResponse.model_validate(categorya)

    async def list_categories(self, include_archived: bool = False) -> list[CategoryResponse]:
        list_of_categories = await self.repository.list_all(include_archived=include_archived)
        return [CategoryResponse.model_validate(cat) for cat in list_of_categories]

    async def update_category(self, category_id: int, data: CategoryUpdate) -> CategoryResponse | None:
        categoria = await self.repository.update(category_id=category_id,data=data)
        if not categoria:
            return None
        return CategoryResponse.model_validate(categoria)

    async def delete_category(self, category_id: int) -> bool:
        categoria = await self.repository.delete(category_id)
        if not categoria:
            return False
        return True


    async def archive_category(self,category_id: int)-> CategoryResponse | None:
            return await self.update_category(category_id, CategoryUpdate(is_archived=True))

