from pydantic import BaseModel, Field, SecretStr


class UserRequest(BaseModel):
    username: str = Field(description="Имя пользователя")
    email: str = Field(description="Email")
    password: SecretStr


class UserResponse(BaseModel):
    id: int
    username: str = Field(description="Имя пользователя")
    email: str = Field(description="Email")
