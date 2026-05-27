from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import CommentNotFound
from src.infrastructure.models.commentsModel import Comment


class CommentRepository:
    def __init__(self):
        self._model: type[Comment] = Comment

    async def get_by_id(
        self, session: AsyncSession, comment_id: int
    ) -> Comment | None:
        comment = await session.scalar(
            select(self._model).where(self._model.id == comment_id)
        )
        if not comment:
            raise CommentNotFound()
        return comment

    async def get_all(self, session: AsyncSession) -> list[Comment]:
        result = await session.scalars(select(self._model))
        return list(result.all())

    async def get_by_post(
        self, session: AsyncSession, post_id: int
    ) -> list[Comment]:
        result = await session.scalars(
            select(self._model).where(self._model.post_id == post_id)
        )
        return list(result.all())

    async def create(
        self,
        session: AsyncSession,
        text: str,
        author_id: int,
        post_id: int,
    ) -> Comment:
        comment = self._model(
            text=text,
            author_id=author_id,
            post_id=post_id,
        )
        session.add(comment)
        await session.flush()
        return comment

    async def delete(
        self, session: AsyncSession, comment_id: int
    ) -> None:
        comment = await self.get_by_id(session, comment_id)
        if comment:
            session.delete(comment)
            await session.flush()
