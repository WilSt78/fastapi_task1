from sqlalchemy.orm import Session
from typing import Optional
import logging
from fastapi import HTTPException
from ...infrastructure.sqlite.repositories.users import UserRepository
from ...schemas.Users import UserRequest, UserResponse
from ...infrastructure.sqlite.database import database 
from ...core.exceptions.domain_exceptions import UserNotFoundByIdException, UserNotFoundByUsernameException, AlreadyOccupied
from ...core.exceptions.database_exceptions import UserNotFoundById, UserNotFoundByUsername, UsernameIsOccupied, EmailIsOccupied, AlreadyExists
logger = logging.getLogger(__name__)

class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[UserResponse]:
        with self._database.session() as session:
            users = self._repo.get_all(session)
            return [UserResponse.model_validate(user) for user in users]

class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.get_detail(session, user_id)
                return UserResponse.model_validate(user)
            except UserNotFoundById:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(error.get_detail())
                raise error


class GetUserByUsernameUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, username: str) -> UserResponse:

        with self._database.session() as session:
            try:
                user = self._repo.get_by_username(session, username)
                return UserResponse.model_validate(user)
            except UserNotFoundByUsername:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(error.get_detail())
                raise error


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_data: UserRequest) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.create(session, user_data)
                return UserResponse.model_validate(user)
            except AlreadyExists as e:
                logger.error(e)
                raise AlreadyOccupied

                


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int,
                    user_data: UserRequest) -> UserResponse:
        with self._database.session() as session:
            try:
                user = self._repo.update(session, user_id, user_data)
                return UserResponse.model_validate(user)
            except (UsernameIsOccupied,EmailIsOccupied, UserNotFoundById) as e:
                logger.error(e.get_detail())
                raise e

class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int) -> dict:
        with self._database.session() as session:
            self.repository.destroy(session, user_id)
            return {"message": "Пользователь успешно удален"}
