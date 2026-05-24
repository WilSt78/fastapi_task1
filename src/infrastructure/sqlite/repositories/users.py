from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
import logging
from sqlalchemy.exc import IntegrityError
from ...sqlite.models.userModel import User
from ....schemas.Users import UserRequest
from ....functions.verify_password import get_password_hash
from ....core.exceptions.database_exceptions import UsernameIsOccupied, EmailIsOccupied, UserNotFoundById, UserNotFoundByUsername, AlreadyExists

logger = logging.getLogger(__name__)


class UserRepository:
    
    async def get_all(self, db: AsyncSession) -> list[User]:
        result = await db.execute(select(User))
        return result.scalars().all()

    async def get_by_username(self, db: AsyncSession, username: str) -> User:
        result = await db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()
        if not user:
            e = UserNotFoundByUsername(username=username)
            logger.error(e.get_detail())
            raise e
        return user

    async def get_detail(self, db: AsyncSession, user_id: int) -> User:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            e = UserNotFoundById(id=user_id)
            logger.error(e.get_detail())
            raise e
        return user

    async def create(self, db: AsyncSession, user_data: UserRequest) -> User:
        try:
            user = User(
                username=user_data.username,
                email=user_data.email,
                password=get_password_hash(user_data.password)
            )
            db.add(user)
            await db.flush()
            await db.refresh(user)
            return user
        except IntegrityError:
            raise AlreadyExists

    async def update(self, db: AsyncSession, user_id: int, user_data: UserRequest) -> User:
        user = await self.get_detail(db, user_id)

        if user_data.username != user.username:
            result = await db.execute(select(User).where(User.username == user_data.username))
            if result.scalar_one_or_none():
                e = UsernameIsOccupied(user_data.username)
                logger.error(e.get_detail())
                raise e

        if user_data.email != user.email:
            result = await db.execute(select(User).where(User.email == user_data.email))
            if result.scalar_one_or_none():
                e = EmailIsOccupied(user_data.email)
                logger.error(e.get_detail())
                raise e

        user.username = user_data.username
        user.email = user_data.email
        user.password = get_password_hash(user_data.password)   
        await db.commit()
        await db.refresh(user)
        return user

    async def destroy(self, db: AsyncSession, user_id: int):
        user = await self.get_detail(db, user_id)
        await db.delete(user)
        await db.commit()