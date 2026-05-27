# src/domain/comments/use_cases/create_comment.py
from src.core.exceptions.database_exceptions import (
    PostNotFound,
    UserNotFound,
)
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.comments import (
    CommentRepository,
)
from src.infrastructure.repositories.posts import (
    PostRepository,
)
from src.infrastructure.repositories.users import (
    UserRepository,
)
from src.schemas.comments import Comment


class CreateCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._user_repo = UserRepository()
        self._post_repo = PostRepository()

    async def execute(
        self, text: str, author_id: int, post_id: int
    ) -> Comment:
        async with self._database.session() as session:
            try:
                await self._user_repo.get_by_id(session, author_id)
                await self._post_repo.get_by_id(session, post_id)
                comment = await self._repo.create(
                    session, text, author_id, post_id
                )
                return Comment.model_validate(comment)
            except UserNotFound as err:
                raise UserNotFoundByIdException(id=author_id) from err
            except PostNotFound as err:
                raise PostNotFoundByIdException(id=post_id) from err


from src.core.exceptions.database_exceptions import CommentNotFound
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.comments import (
    CommentRepository,
)


class DeleteCommentUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> None:
        try:
            async with self._database.session() as session:
                comment = await self._repo.get_by_id(
                    session, comment_id
                )
        except CommentNotFound as err:
            raise CommentNotFoundByIdException(
                comment_id=comment_id
            ) from err
        self._repo.delete(session, comment)
        session.commit()


from src.infrastructure.database import database
from src.infrastructure.repositories.comments import (
    CommentRepository,
)
from src.schemas.comments import Comment


class GetAllCommentsUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self) -> list[Comment]:
        async with self._database.session() as session:
            comments = await self._repo.get_all(session)
            return [Comment.model_validate(post) for post in comments]


from src.core.exceptions.database_exceptions import CommentNotFound
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.comments import (
    CommentRepository,
)
from src.schemas.comments import Comment


class GetCommentByIdUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()

    async def execute(self, comment_id: int) -> Comment:
        async with self._database.session() as session:
            try:
                comment = await self._repo.get_by_id(
                    session, comment_id
                )
                return Comment.model_validate(comment)
            except CommentNotFound as err:
                raise CommentNotFoundByIdException(
                    comment_id=comment_id
                ) from err


from src.core.exceptions.database_exceptions import PostNotFound
from src.core.exceptions.domain_exceptions import (
    PostNotFoundByIdException,
)
from src.infrastructure.database import database
from src.infrastructure.repositories.comments import (
    CommentRepository,
)
from src.infrastructure.repositories.posts import (
    PostRepository,
)
from src.schemas.comments import Comment


class GetCommentsByPostUseCase:
    def __init__(self):
        self._database = database
        self._repo = CommentRepository()
        self._post_repo = PostRepository()

    async def execute(self, post_id: int) -> list[Comment]:
        async with self._database.session() as session:
            try:
                await self._post_repo.get_by_id(session, post_id)
                comments = await self._repo.get_by_post(
                    session, post_id
                )
                return comments
            except PostNotFound as err:
                raise PostNotFoundByIdException(id=post_id) from err
