from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .postsModel import Post


class Location(Base):
    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )

    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="location"
    )
