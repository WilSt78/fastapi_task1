from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .commentsModel import Comment
    from .postsModel import Post


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(100), unique=True, nullable=False
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)

    posts: Mapped[list[Post]] = relationship(
        "Post", back_populates="author"
    )
    comments: Mapped[list[Comment]] = relationship(
        "Comment", back_populates="author"
    )
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)
