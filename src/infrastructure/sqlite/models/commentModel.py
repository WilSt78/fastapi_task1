from datetime import datetime
from sqlalchemy import Text, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .baseModel import Base


class Comment(Base):
    __tablename__ = 'comments'

    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(
        Text
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now
    )

    post_id: Mapped[int] = mapped_column(
        ForeignKey('posts.id', ondelete='CASCADE')
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('users.id', ondelete='CASCADE')
    )
    post = relationship('Post',
                        back_populates='comments'
                        )
    author = relationship('User',
                          back_populates='comments'
                          )
