from pydantic import Field

from .base import Base


class Location(Base):
    id: int
    name: str = Field(max_length=200)
