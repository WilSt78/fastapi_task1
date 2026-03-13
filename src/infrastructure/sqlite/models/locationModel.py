from datetime import datetime
from typing import List
from sqlalchemy import String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .baseModel import Base
from .postModel import Post

TEXT_LENGTH = 256


class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(
        String(TEXT_LENGTH)
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
                         back_populates='location',
                         cascade='all, delete-orphan'
                         )
