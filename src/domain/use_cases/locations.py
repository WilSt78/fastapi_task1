import logging

from src.core.exceptions.database_exceptions import LocationAlreadyExists, LocationNotFound
from src.core.exceptions.domain_exceptions import (
    LocationNameIsOccupiedException,
    LocationNotFoundByIdException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.locations import LocationRepository
from src.schemas.locations import Location

logger = logging.getLogger(__name__)


class CreateLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, name: str) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.create(session, name)
                logger.info(f"Локация создана: id={location.id}, name={location.name}")
                return Location.model_validate(location)
            except LocationAlreadyExists as err:
                error = LocationNameIsOccupiedException(name=name)
                logger.error(error.detail)
                raise error from err


class DeleteLocationUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> None:
        async with self._database.session() as session:
            try:
                await self._repo.get_by_id(session, location_id)
            except LocationNotFound as err:
                error = LocationNotFoundByIdException(id=location_id)
                logger.error(error.detail)
                raise error from err

            await self._repo.delete(session, location_id)
            logger.info(f"Локация {location_id} удалена")


class GetAllLocationsUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self) -> list[Location]:
        async with self._database.session() as session:
            locations = await self._repo.get_all(session)
            return [Location.model_validate(location) for location in locations]


class GetLocationByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = LocationRepository()

    async def execute(self, location_id: int) -> Location:
        async with self._database.session() as session:
            try:
                location = await self._repo.get_by_id(session, location_id)
                return Location.model_validate(location)
            except LocationNotFound as err:
                error = LocationNotFoundByIdException(location_id=location_id)
                logger.error(error.detail)
                raise error from err