import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    CategoryAlreadyExists,
    CategoryNotFound,
)
from src.infrastructure.models.categoriesModel import (
    Category,
)

logger = logging.getLogger(__name__)


class CategoryRepository:
    def __init__(self):
        self._model: type[Category] = Category

    async def get_by_id(
        self, session: AsyncSession, category_id: int
    ) -> Category:
        category = await session.scalar(
            select(self._model).where(self._model.id == category_id)
        )
        if not category:
            raise CategoryNotFound()
        return category

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Category | None:
        result = await session.scalar(
            select(self._model).where(self._model.title == name)
        )
        return result

    async def get_all(self, session: AsyncSession) -> list[Category]:
        result = await session.scalars(select(self._model))
        return list(result.all())

    async def create(
        self,
        session: AsyncSession,
        title: str,
        description: str,
        slug: str,
    ) -> Category:
        try:
            category = self._model(
                title=title, description=description, slug=slug
            )
            session.add(category)
            await session.flush()
            return category
        except IntegrityError as err:
            raise CategoryAlreadyExists() from err

    async def delete(
        self, session: AsyncSession, category_id: int
    ) -> None:
        category = await self.get_by_id(session, category_id)
        session.delete(category)
        await session.flush()
