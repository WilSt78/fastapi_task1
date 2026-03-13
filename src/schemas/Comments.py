from .Base import Base
from pydantic import Field
from .Posts import Post
from .Users import UserRequest
from datetime import date, datetime


class Comment(Base):
    text: str = Field(description="Текст комментария")
    post: Post = Field(description="Комментарий")
    created_at: date = Field(default_factory=datetime.now)
    author: UserRequest
