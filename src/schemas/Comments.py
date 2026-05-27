from datetime import datetime

from pydantic import Field

from src.schemas.base import Base


class Comment(Base):
    text: str = Field(max_length=100)
    author_id: int
    created: datetime = Field(default_factory=datetime.now)
    post_id: int
