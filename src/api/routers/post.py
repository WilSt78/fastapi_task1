from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_post_use_case,
    delete_post_use_case,
    get_all_posts_use_case,
    get_post_by_id_use_case,
    update_post_use_case,
)
from src.core.exceptions.domain_exceptions import (
    CategoryNotFoundByIdException,
    LocationNotFoundByIdException,
    PermissionDeniedException,
    PostNotFoundByIdException,
    UserNotFoundByIdException,
)
from src.domain.use_cases.posts import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetAllPostsUseCase,
    GetPostByIdUseCase,
    UpdatePostUseCase,
)
from src.schemas.posts import PostRequest, PostResponse
from src.services.auth import AuthService

router = APIRouter()


@router.get(
    "/posts",
    response_model=list[PostResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_posts(
    use_case: GetAllPostsUseCase = Depends(get_all_posts_use_case),
):
    return await use_case.execute()


@router.get(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def get_post_by_id(
    post_id: int,
    use_case: GetPostByIdUseCase = Depends(get_post_by_id_use_case),
):
    try:
        return await use_case.execute(post_id)
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.post(
    "/posts",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    post_data: PostRequest,
    current_user=Depends(AuthService.get_current_user),
    use_case: CreatePostUseCase = Depends(create_post_use_case),
):
    try:
        return await use_case.execute(
            post_data, current_user.id, current_user.username
        )
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc


@router.put(
    "/posts/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
)
async def update_post(
    post_id: int,
    post_data: PostRequest,
    current_user=Depends(AuthService.get_current_user),
    use_case: UpdatePostUseCase = Depends(update_post_use_case),
):
    try:
        return await use_case.execute(
            post_id, post_data, current_user.id
        )
    except PostNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except LocationNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except CategoryNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except PermissionDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        ) from exc


@router.delete(
    "/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_post(
    post_id: int,
    current_user=Depends(AuthService.get_current_user),
    use_case: DeletePostUseCase = Depends(delete_post_use_case),
):
    try:
        await use_case.execute(post_id, current_user.id)
    except PostNotFoundByIdException as exc:
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
