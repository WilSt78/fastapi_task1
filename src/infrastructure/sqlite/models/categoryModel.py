from datetime import datetime
from typing import List
from sqlalchemy import String, Text, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .baseModel import Base


TEXT_LENGTH = 256


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(TEXT_LENGTH)
    )
    description: Mapped[str] = mapped_column(
        Text
    )
    slug: Mapped[str] = mapped_column(
        String(TEXT_LENGTH),
        unique=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    posts = relationship('Post',
                         back_populates='category',
                         cascade='all, delete-orphan'
                         )
