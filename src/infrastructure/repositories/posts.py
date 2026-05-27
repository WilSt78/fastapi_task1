import logging

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions.database_exceptions import (
    CategoryNotFound,
    LocationNotFound,
    PostNotFound,
    UserNotFound,
)
from src.core.utils.db_error import parse_integrity_error
from src.infrastructure.models.postsModel import Post
from src.schemas.posts import PostRequest

logger = logging.getLogger(__name__)


class PostRepository:
    def __init__(self):
        self._model: type[Post] = Post

    async def get_by_id(
        self, session: AsyncSession, post_id: int
    ) -> Post:
        post = await session.scalar(
            select(self._model).where(self._model.id == post_id)
        )
        if not post:
            raise PostNotFound()
        return post

    async def get_all(self, session: AsyncSession) -> list[Post]:
        result = await session.scalars(select(self._model))
        return list(result.all())

    async def get_by_author(
        self, session: AsyncSession, author_id: int
    ) -> list[Post]:
        result = await session.scalars(
            select(self._model).where(
                self._model.author_id == author_id
            )
        )
        posts = list(result.all())
        return posts

    async def create(
        self,
        session: AsyncSession,
        title: str,
        text: str,
        author_id: int,
        location_id: int | None = None,
        category_id: int | None = None,
    ) -> Post:
        try:
            post = self._model(
                title=title,
                text=text,
                author_id=author_id,
                location_id=location_id,
                category_id=category_id,
            )
            session.add(post)
            await session.flush()
            return post
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "author_id":
                raise UserNotFound() from err
            elif final_cause == "location_id":
                raise LocationNotFound() from err
            elif final_cause == "category_id":
                raise CategoryNotFound() from err
            else:
                logger.error(f"Unexpected integrity error: {err}")
                raise err

    async def update(
        self,
        session: AsyncSession,
        post_id: int,
        post_data: PostRequest,
    ) -> Post:
        post = await self.get_by_id(session, post_id)
        post.title = post_data.title
        post.text = post_data.text
        if (
            post_data.location_id
            and post_data.location_id != post.location_id
        ):
            post.location_id = post_data.location_id
        if (
            post_data.category_id
            and post_data.category_id != post.category_id
        ):
            post.category_id = post_data.category_id
        try:
            await session.flush()
            await session.refresh(post)
            return post
        except IntegrityError as err:
            final_cause = parse_integrity_error(err)
            if final_cause == "location_id":
                raise LocationNotFound() from err
            elif final_cause == "category_id":
                raise CategoryNotFound() from err

    async def delete(
        self, session: AsyncSession, post_id: int
    ) -> None:
        post = await self.get_by_id(session, post_id)
        session.delete(post)
        await session.flush()
