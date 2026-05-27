from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .postsModel import Post


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    description: Mapped[str] = mapped_column(
        String(150), nullable=True
    )
    slug: Mapped[str] = mapped_column(
        String(150), unique=True, nullable=False
    )

    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="category"
    )
