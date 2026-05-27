from typing import Annotated

from fastapi import Depends
from jose import JWTError, jwt
from pydantic import SecretStr

from src.core.exceptions.auth_exceptions import CredentialException
from src.core.exceptions.database_exceptions import UserNotFound
from src.infrastructure.database import Database
from src.infrastructure.database import (
    database as postgres_database,
)
from src.infrastructure.repositories.users import (
    UserRepository,
)
from src.resources.auth import oauth2_scheme
from src.schemas.users import LoginUserResponse

AUTH_EXCEPTION_MESSAGE = "Невозможно проверить данные авторизации"
SECRET_AUTH_KEY = SecretStr(
    "VEwth77AYpePfG1xShbAKR__o0wuKpes5Yzjqjrcgww"
)
AUTH_ALGORITHM = "HS256"


class AuthService:
    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
    ):
        __database: Database = postgres_database
        __repo: UserRepository = UserRepository()

        try:
            payload = jwt.decode(
                token=token,
                key=SECRET_AUTH_KEY.get_secret_value(),
                algorithms=[AUTH_ALGORITHM],
            )
            username: str = payload.get("sub")
            if username is None:
                raise CredentialException(
                    detail=AUTH_EXCEPTION_MESSAGE
                )
        except JWTError as err:
            raise CredentialException(
                detail=AUTH_EXCEPTION_MESSAGE
            ) from err

        try:
            async with __database.session() as session:
                user = await __repo.get_by_username(
                    session=session, username=username
                )
                if user is None:
                    raise CredentialException(
                        detail="Сессия устарела. Пожалуйста, войдите заново."
                    )
                return LoginUserResponse.model_validate(obj=user)
        except UserNotFound as exc:
            raise CredentialException(
                detail=AUTH_EXCEPTION_MESSAGE
            ) from exc
