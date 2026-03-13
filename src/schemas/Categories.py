from .Base import Base
from pydantic import Field


TEXT_LENGTH = 256


class Category(Base):
    title: str = Field(max_length=TEXT_LENGTH,
                       description="Заголовок")
    description: str = Field(description="Описание")
    slug: str
