import logging

from src.core.exceptions.database_exceptions import UserAlreadyExists, UserNotFound
from src.core.exceptions.domain_exceptions import (
    PermissionDeniedException,
    UsernameIsOccupiedException,
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.domain.use_cases.auth import CreateAccessTokenUseCase
from src.infrastructure.database import database
from src.infrastructure.repositories.users import UserRepository
from src.resources.auth import get_password_hash, verify_password
from src.schemas.users import (
    LoginUserResponse,
    RegisterUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
)

logger = logging.getLogger(__name__)


class CreateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user: RegisterUserRequest) -> LoginUserResponse:
        user.password = get_password_hash(password=user.password)
        async with self._database.session() as session:
            try:
                user1 = await self._repo.create(session, user)
            except UserAlreadyExists as err:
                error = UsernameIsOccupiedException(username=user.username)
                logger.error(error.detail)
                raise error from err
            return LoginUserResponse.model_validate(obj=user1)


class DeleteUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, username: str, cur_user: LoginUserResponse, password: str
    ) -> None:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_username(session, username)
            except UserNotFound as exc:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(error.detail)
                raise error from exc

            if cur_user.is_admin:
                await self._repo.delete(session, user.id)
                return

            if cur_user.username != username:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error

            if not verify_password(password, user.password):
                error = WrongPasswordException()
                logger.error(error.detail)
                raise error

            await self._repo.delete(session, user.id)


class GetAllUsersUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self) -> list[LoginUserResponse]:
        async with self._database.session() as session:
            users = await self._repo.get_all(session=session)
            return [LoginUserResponse.model_validate(obj=user) for user in users]


class GetUserByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()

    async def execute(self, user_id: int, cur_user: LoginUserResponse) -> LoginUserResponse:
        async with self._database.session() as session:
            try:
                user = await self._repo.get_by_id(session, user_id)
                return LoginUserResponse.model_validate(user)
            except UserNotFound as err:
                error = UserNotFoundByIdException(id=user_id)
                logger.error(f"Пользователь {cur_user.username} произвел ошибку: {error.detail}")
                raise error from err


class UpdateUserUseCase:
    def __init__(self):
        self._database = database
        self._repo = UserRepository()
        self._token_use_case = CreateAccessTokenUseCase()

    async def execute(
        self,
        username: str,
        user_data: UpdateUserRequest,
        current_user: LoginUserResponse,
    ) -> UpdateUserResponse:
        async with self._database.session() as session:
            user = await self._repo.get_by_username(session, username)
            if not user:
                error = UserNotFoundByUsernameException(username=username)
                logger.error(error.detail)
                raise error

            if current_user.username != username:
                error = PermissionDeniedException()
                logger.error(error.detail)
                raise error

            if not verify_password(user_data.current_password, user.password):
                error = WrongPasswordException()
                logger.error(error.detail)
                raise error

            if user_data.new_username and user_data.new_username != user.username:
                existing = await self._repo.get_by_username(session, user_data.new_username)
                if existing:
                    error = UsernameIsOccupiedException(username=user_data.new_username)
                    logger.error(error.detail)
                    raise error
                user.username = user_data.new_username

            if user_data.new_password:
                user.password = get_password_hash(user_data.new_password)

            await session.commit()
            await session.refresh(user)

            new_token = await self._token_use_case.execute(username=user.username)

            return UpdateUserResponse(
                user=LoginUserResponse.model_validate(user),
                access_token=new_token,
                token_type="bearer",
            )