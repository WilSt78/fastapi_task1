from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_category_use_case,
    delete_category_use_case,
    get_all_categories_use_case,
    get_category_by_id_use_case,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsOccupiedException,
)
from src.domain.use_cases.categories import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetAllCategoriesUseCase,
    GetCategoryByIdUseCase,
)
from src.schemas.categories import Category
from src.services.auth import AuthService

router = APIRouter()


@router.get(
    "/categories",
    response_model=list[Category],
    status_code=status.HTTP_200_OK,
)
async def get_all_categories(
    use_case: GetAllCategoriesUseCase = Depends(
        get_all_categories_use_case
    ),
):
    return await use_case.execute()


@router.get(
    "/categories/{category_id}",
    response_model=Category,
    status_code=status.HTTP_200_OK,
)
async def get_category_by_id(
    category_id: int,
    use_case: GetCategoryByIdUseCase = Depends(
        get_category_by_id_use_case
    ),
):
    try:
        return await use_case.execute(category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.post(
    "/categories",
    response_model=Category,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    title: str,
    slug: str,
    description: str = None,
    current_user=Depends(AuthService.get_current_user),
    use_case: CreateCategoryUseCase = Depends(
        create_category_use_case
    ),
):
    try:
        return await use_case.execute(title, slug, description)
    except CategorySlugIsOccupiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        ) from exc


@router.delete(
    "/categories/{category_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_category(
    category_id: int,
    current_user=Depends(AuthService.get_current_user),
    use_case: DeleteCategoryUseCase = Depends(
        delete_category_use_case
    ),
):
    try:
        await use_case.execute(category_id)
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    return None
