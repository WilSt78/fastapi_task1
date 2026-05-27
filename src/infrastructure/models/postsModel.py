from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .categoriesModel import Category
    from .commentsModel import Comment
    from .locationsModel import Location
    from .usersModel import User


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(150), nullable=False)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    published: Mapped[bool] = mapped_column(Boolean, default=True)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    location_id: Mapped[int | None] = mapped_column(
        ForeignKey("locations.id"), nullable=True
    )
    category_id: Mapped[int | None] = mapped_column(
        ForeignKey("categories.id"), nullable=True
    )

    author: Mapped[User] = relationship(
        "User", back_populates="posts"
    )
    location: Mapped[Location | None] = relationship(
        "Location", back_populates="posts"
    )
    category: Mapped[Category | None] = relationship(
        "Category", back_populates="posts"
    )
    comments: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="post", cascade="all, delete-orphan"
    )
