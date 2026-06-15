import logging

from src.core.exceptions.database_exceptions import CategoryAlreadyExists, CategoryNotFound
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    CategorySlugIsOccupiedException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.categories import CategoryRepository
from src.schemas.categories import Category

logger = logging.getLogger(__name__)


class CreateCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, title: str, slug: str, description: str = None) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.create(session, title, description, slug)
                return Category.model_validate(category)
            except CategoryAlreadyExists as err:
                error = CategorySlugIsOccupiedException(slug=slug)
                logger.error(error.detail)
                raise error from err


class DeleteCategoryUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.get_by_id(session, category_id)
            except CategoryNotFound as err:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.detail)
                raise error from err

            await self._repo.delete(session, category_id)


class GetAllCategoriesUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self) -> list[Category]:
        async with self._database.session() as session:
            categories = await self._repo.get_all(session)
            return [Category.model_validate(category) for category in categories]


class GetCategoryByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CategoryRepository()

    async def execute(self, category_id: int) -> Category:
        async with self._database.session() as session:
            try:
                category = await self._repo.get_by_id(session, category_id)
                return Category.model_validate(category)
            except CategoryNotFound as err:
                error = CategoryNotFoundByIdException(category_id=category_id)
                logger.error(error.detail)
                raise error from err