from pydantic import Field

from .base import Base


class Category(Base):
    id: int
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=500)
    slug: str = Field(default=None, max_length=200)
