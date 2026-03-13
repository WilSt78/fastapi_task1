from datetime import datetime
from typing import Optional
from sqlalchemy import String, Text, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .baseModel import Base


TEXT_LENGTH = 256


class Post(Base):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(TEXT_LENGTH)
    )
    text: Mapped[str] = mapped_column(
        Text
    )
    pub_date: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    image: Mapped[Optional[str]] = mapped_column(
        String(500),
        nullable=True
    )
    is_published: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    location_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('locations.id', ondelete='SET NULL'),
        nullable=True
    )
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True
    )
    author = relationship('User',
                          back_populates='posts'
                          )
    location = relationship('Location',
                            back_populates='posts'
                            )
    category = relationship('Category',
                            back_populates='posts'
                            )
    comments = relationship('Comment',
                            back_populates='post',
                            cascade='all, delete-orphan'
                            )
