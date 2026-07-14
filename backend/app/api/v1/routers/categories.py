
from app.api.v1.dependencies import  get_category_service
from fastapi import Depends, APIRouter, status
from app.services import  CategoryService
from app.schemas import CategoryResponse, CategoryUpdate, CategoryCreate

router = APIRouter(prefix="/categories", tags=["categories"])   #  prefix — все пути начнутся с /categories. tags — группировка в Swagger.

@router.post('', status_code=status.HTTP_201_CREATED)
async def create_category(data:CategoryCreate, service: CategoryService = Depends(get_category_service)) -> CategoryResponse:
    return await service.create_category(data=data)

@router.get('/{category_id}')
async def get_category(category_id: int, service: CategoryService = Depends(get_category_service)) -> CategoryResponse:
    result = await service.get_category(category_id)
    return result

@router.get('', response_model=list[CategoryResponse])
async def list_categories(service: CategoryService = Depends(get_category_service)) -> list[CategoryResponse]:
    return await service.list_categories()



@router.patch('/{category_id}')
async def update_category(category_id: int,
                          data: CategoryUpdate,
                          service: CategoryService = Depends(get_category_service)) -> CategoryResponse:
    result = await service.update_category(category_id=category_id, data=data)
    return result


@router.delete('/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(category_id: int,
                          service: CategoryService = Depends(get_category_service)):
    await service.delete_category(category_id=category_id)



@router.post("/{category_id}/archive")
async def archive_category(category_id: int,
                          service: CategoryService = Depends(get_category_service)) -> CategoryResponse:
    result = await service.archive_category(category_id=category_id)
    return result



