from datetime import datetime, timedelta, timezone
from jose import jwt

from ...functions.verify_password import verify_password
from ...settings import TOKEN_EXPIRE_TIME, SECRET_KEY, ALGORITHM
from ...infrastructure.sqlite.database import database 
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.Users import UserResponse
from ...core.exceptions.database_exceptions import UserNotFoundByUsername
from ...core.exceptions.domain_exceptions import UserNotFoundByUsernameException, PasswordsDoesntMatch


class CreateAccessTokenUseCase:
    def execute(
            self, nickname: str,
            expires_delta: timedelta | None = None
        ) -> str:
        to_encode = {"sub": nickname}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_TIME)

        to_encode["exp"] = expire
        encoded_jwt = jwt.encode(
            to_encode,
            key=SECRET_KEY.get_secret_value(),
            algorithm=ALGORITHM,
        )

        return encoded_jwt


class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()
        self._database = database

    def execute(self, username: str, password: str) -> UserResponse:
        with self._database.session() as session:
            try:
                user_model = self._repo.get_by_username(session, username) 
            except UserNotFoundByUsername:
                raise UserNotFoundByUsernameException(username)
            
            if not verify_password(password, user_model.password):
                return UserResponse.model_validate(user_model)
            raise PasswordsDoesntMatch