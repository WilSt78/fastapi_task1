from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.infrastructure.database import Base

if TYPE_CHECKING:
    from .postsModel import Post
    from .usersModel import User


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(100), nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    author_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )
    post_id: Mapped[int] = mapped_column(
        ForeignKey("posts.id"), nullable=False
    )

    author: Mapped[User] = relationship(
        "User", back_populates="comments"
    )
    post: Mapped[Post] = relationship(
        "Post", back_populates="comments"
    )
