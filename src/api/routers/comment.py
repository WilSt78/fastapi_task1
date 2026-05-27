# ruff: noqa: B008
from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_comment_use_case,
    delete_comment_use_case,
    get_all_comments_use_case,
    get_comment_by_id_use_case,
    get_comments_by_post_use_case,
)
from src.core.exceptions.domain_exceptions import (
    CommentNotFoundByIdException,
    PermissionDeniedException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.domain.use_cases.comments import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    GetCommentsByPostUseCase,
)
from src.schemas.comments import Comment
from src.services.auth import AuthService

router = APIRouter()


@router.get(
    "/comments",
    response_model=list[Comment],
    status_code=status.HTTP_200_OK,
)
async def get_all_comments(
    use_case: GetAllCommentsUseCase = Depends(
        get_all_comments_use_case
    ),
):
    return await use_case.execute()


@router.get(
    "/comments/{comment_id}",
    response_model=Comment,
    status_code=status.HTTP_200_OK,
)
async def get_comment_by_id(
    comment_id: int,
    use_case: GetCommentByIdUseCase = Depends(
        get_comment_by_id_use_case
    ),
):
    try:
        return await use_case.execute(comment_id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.get(
    "/comments/by-post/{post_id}",
    response_model=list[Comment],
    status_code=status.HTTP_200_OK,
)
async def get_comments_by_post(
    post_id: int,
    use_case: GetCommentsByPostUseCase = Depends(
        get_comments_by_post_use_case
    ),
):
    try:
        return await use_case.execute(post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.post(
    "/comments",
    response_model=Comment,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    text: str,
    post_id: int,
    current_user=Depends(AuthService.get_current_user),
    use_case: CreateCommentUseCase = Depends(create_comment_use_case),
):
    try:
        return await use_case.execute(text, current_user.id, post_id)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.delete(
    "/comments/{comment_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_comment(
    comment_id: int,
    current_user=Depends(AuthService.get_current_user),
    use_case: DeleteCommentUseCase = Depends(delete_comment_use_case),
):
    try:
        await use_case.execute(comment_id, current_user.id)
    except CommentNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except PermissionDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        ) from exc
    return None
