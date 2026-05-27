from pydantic import Field

from .base import Base


class PostRequest(Base):
    title: str = Field(max_length=200)
    text: str = Field(max_length=2000)
    location_name: str | None = None
    category_name: str | None = None


class PostResponse(Base):
    id: int
    title: str
    text: str
    author_id: int
    location_name: str | None = None
    category_name: str | None = None
