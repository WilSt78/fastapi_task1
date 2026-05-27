import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    LocationAlreadyExists,
    LocationNotFound,
)
from src.infrastructure.models.locationsModel import Location

logger = logging.getLogger(__name__)


class LocationRepository:
    def __init__(self):
        self._model: type[Location] = Location

    async def get_by_id(
        self, session: AsyncSession, location_id: int
    ) -> Location:
        location = await session.scalar(
            select(self._model).where(self._model.id == location_id)
        )
        if not location:
            raise LocationNotFound()
        return location

    async def get_by_name(
        self, session: AsyncSession, name: str
    ) -> Location | None:
        return await session.scalar(
            select(self._model).where(self._model.name == name)
        )

    async def get_all(self, session: AsyncSession) -> list[Location]:
        result = await session.scalars(select(self._model))
        return list(result.all())

    async def create(
        self, session: AsyncSession, name: str
    ) -> Location:
        try:
            location = self._model(name=name)
            session.add(location)
            await session.flush()
            return location
        except IntegrityError as err:
            raise LocationAlreadyExists() from err

    async def delete(
        self, session: AsyncSession, location_id: int
    ) -> None:
        location = await self.get_by_id(session, location_id)
        if location:
            session.delete(location)
            await session.flush()
