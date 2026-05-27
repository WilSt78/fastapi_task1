from fastapi import HTTPException, status
from pydantic import (
    BaseModel,
    ConfigDict,
    field_validator,
    model_validator,
)


class RegisterUserRequest(BaseModel):
    username: str
    password: str

    @model_validator(mode="after")
    def validate_request(self) -> "RegisterUserRequest":
        if not self.username:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Необходимо ввести username",
            )
        return self

    @field_validator("password")
    @staticmethod
    def check_password(password: str) -> str:
        passw = password
        if len(passw) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Длина пароля должна быть как минимум 8 символов",
            )
        if not any(c.islower() for c in passw) or not any(
            c.isupper() for c in passw
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Пароль должен содержать и строчные, и заглавные буквы",
            )
        return password


class LoginUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    is_admin: bool = False


class UpdateUserRequest(BaseModel):
    current_password: str
    new_username: str | None = None
    new_password: str | None = None

    @field_validator("new_password")
    @staticmethod
    def check_new_password(password: str | None) -> str | None:
        if password is None:
            return password
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Новый пароль должен содержать минимум 8 символов",
            )
        if not any(c.islower() for c in password) or not any(
            c.isupper() for c in password
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Новый пароль должен содержать и строчные, и заглавные буквы",
            )
        return password


class UpdateUserResponse(BaseModel):
    user: LoginUserResponse
    access_token: str
    token_type: str = "bearer"


class DeleteUserRequest(BaseModel):
    password: str
