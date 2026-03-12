from pydantic import BaseModel, Field
from datetime import date


TEXT_LENGTH = 256


class Base(BaseModel):
    is_published: bool = Field(default=True,
                               description="Опубликовано")
    created_at: date = Field(description="Добавлено")
