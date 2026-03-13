from .Base import Base
from pydantic import Field


TEXT_LENGTH = 256


class Location(Base):
    name: str = Field(max_length=TEXT_LENGTH,
                      description="Название места")
