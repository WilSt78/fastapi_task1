from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from ...functions.verify_password import verify_password
from ...config import settings
from ...infrastructure.sqlite.database import database 
from src.infrastructure.sqlite.repositories.users import UserRepository
from src.schemas.Users import UserResponse
from ...core.exceptions.database_exceptions import UserNotFoundByUsername
from ...core.exceptions.domain_exceptions import UserNotFoundByUsernameException, PasswordsDoesntMatch, InvalidTokenException

security = HTTPBearer()

class CreateAccessTokenUseCase:
    def execute(
        self, 
        nickname: str,
        expires_delta: timedelta | None = None
    ) -> str:
        to_encode = {"sub": nickname}
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=settings.TOKEN_EXPIRE_TIME)

        to_encode["exp"] = expire
        encoded_jwt = jwt.encode(
            to_encode,
            key=settings.SECRET_KEY.get_secret_value(),
            algorithm=settings.ALGORITHM,
        )
        return encoded_jwt
    
class AuthenticateUserUseCase:
    def __init__(self) -> None:
        self._repo = UserRepository()
        self._database = database

    async def execute(self, username: str, password: str) -> UserResponse: 
        async with self._database.session() as session:  
            try:
                user_model = await self._repo.get_by_username(session, username) 
            except UserNotFoundByUsername:
                raise UserNotFoundByUsernameException(username)
            
            if verify_password(password, user_model.password):
                return UserResponse.model_validate(user_model)
            raise PasswordsDoesntMatch()
        
class GetCurrentUserUseCase:
    
    def __init__(self):
        self._database = database
        self._repo = UserRepository()
    
    async def execute(self, token: str) -> UserResponse: 
        if token.startswith("Bearer "):
            token = token.replace("Bearer ", "")
        
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY.get_secret_value(),
                algorithms=[settings.ALGORITHM]
            )
        except JWTError:
            raise InvalidTokenException()
        
        username = payload.get("sub")
        if not username:
            raise InvalidTokenException()
        
        async with self._database.session() as session: 
            try:
                user = await self._repo.get_by_username(session, username) 
            except UserNotFoundByUsername:
                raise UserNotFoundByUsernameException(username)
        
            return UserResponse.model_validate(user)