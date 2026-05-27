import logging

from src.core.exceptions.domain_exceptions import (
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.users import (
    UserRepository,
)
from src.resources.auth import verify_password
from src.schemas.users import LoginUserResponse
from datetime import UTC, datetime, timedelta

from jose import jwt

from src.services.auth import AUTH_ALGORITHM, SECRET_AUTH_KEY

logger = logging.getLogger(__name__)


class AuthenticateUseCase:
    def __init__(self) -> None:
        self._database = database
        self._repo = UserRepository()

    async def execute(
        self, username: str, password: str
    ) -> LoginUserResponse:

        async with self._database.session() as session:
            user = await self._repo.get_by_username(session, username)

            if not user:
                error = UserNotFoundByUsernameException(
                    username=username
                )
                logger.error(str(error))
                raise error

            if not verify_password(password, user.password):
                error = WrongPasswordException()
                logger.error(str(error))
                raise error

            return LoginUserResponse.model_validate(user)


class CreateAccessTokenUseCase:
    def __init__(self, token_expire_minutes: int = 10) -> None:
        self._ACCESS_TOKEN_EXPIRE_MINUTES = token_expire_minutes

    async def execute(
        self, username: str, expires_delta: timedelta | None = None
    ) -> str:
        to_encode = {"sub": username}
        if expires_delta:
            expire = datetime.now(UTC) + expires_delta
        else:
            expire = datetime.now(UTC) + timedelta(
                minutes=self._ACCESS_TOKEN_EXPIRE_MINUTES
            )

        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            claims=to_encode,
            key=SECRET_AUTH_KEY.get_secret_value(),
            algorithm=AUTH_ALGORITHM,
        )

        return encoded_jwt
