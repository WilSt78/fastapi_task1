from pydantic import Field, BaseModel


class Token(BaseModel):
    access_token: str = Field()
    token_type: str = Field()