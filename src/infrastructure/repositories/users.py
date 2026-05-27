import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    UserAlreadyExists,
    UserNotFound,
)
from src.core.utils.db_error import parse_integrity_error
from src.infrastructure.models.usersModel import User
from src.schemas.users import RegisterUserRequest

logger = logging.getLogger(__name__)


class UserRepository:
    def __init__(self):
        self._model: type[User] = User

    async def get_by_id(
        self, session: AsyncSession, user_id: int
    ) -> User:
        user = await session.scalar(
            select(self._model).where(self._model.id == user_id)
        )
        if not user:
            raise UserNotFound()
        return user

    async def get_by_username(
        self, session: AsyncSession, username: str
    ) -> User | None:
        result = await session.execute(
            select(self._model).where(
                self._model.username == username
            )
        )
        return result.scalars().first()

    async def get_all(self, session: AsyncSession) -> list[User]:
        result = await session.scalars(select(self._model))
        return list(result.all())

    async def create(
        self, session: AsyncSession, user_data: RegisterUserRequest
    ) -> User:
        try:
            user = self._model(
                username=user_data.username,
                password=user_data.password,
            )
            session.add(user)
            await session.flush()
            return user
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "username":
                raise UserAlreadyExists() from err

    async def update(
        self,
        session: AsyncSession,
        user_id: int,
        user_data: RegisterUserRequest,
    ) -> User:
        user = await self.get_by_id(session, user_id)
        if user_data.username and user_data.username != user.username:
            existing = await self.get_by_username(
                session, user_data.username
            )
            if existing:
                raise UserAlreadyExists()
            user.username = user_data.username
        if user_data.password:
            user.password = user_data.password
        await session.refresh(user)
        return user

    async def delete(
        self, session: AsyncSession, user_id: int
    ) -> None:
        user = await self.get_by_id(session, user_id)
        session.delete(user)
        await session.flush()
