from pydantic import BaseModel, Field

from src.resources.field_description import ACCESS_TOKEN, TOKEN_TYPE


class Token(BaseModel):
    access_token: str = Field(description=ACCESS_TOKEN)
    token_type: str = Field(description=TOKEN_TYPE)


class TokenData(BaseModel):
    user_id: int | None = None


class LoginRequest(BaseModel):
    username: str
    password: str
