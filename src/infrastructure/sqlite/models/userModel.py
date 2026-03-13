from datetime import datetime
from typing import List
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .baseModel import Base


TEXT_LENGTH = 256


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(
        String(TEXT_LENGTH),
        unique=True,
        nullable=False
    )
    email: Mapped[str] = mapped_column(
        String(TEXT_LENGTH),
        unique=True,
        nullable=False
    )
    password: Mapped[str] = mapped_column(String(128))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    posts = relationship('Post',
                         back_populates='author',
                         cascade='all, delete-orphan'
                         )
    comments = relationship('Comment',
                            back_populates='author',
                            cascade='all, delete-orphan'
                            )
