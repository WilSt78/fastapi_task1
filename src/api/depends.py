from src.domain.use_cases.auth import (
    AuthenticateUseCase,
    CreateAccessTokenUseCase,
)

from src.domain.use_cases.categories import (
    CreateCategoryUseCase,
    DeleteCategoryUseCase,
    GetAllCategoriesUseCase,
    GetCategoryByIdUseCase,
)
from src.domain.use_cases.comments import (
    CreateCommentUseCase,
    DeleteCommentUseCase,
    GetAllCommentsUseCase,
    GetCommentByIdUseCase,
    GetCommentsByPostUseCase,
)
from src.domain.use_cases.locations import (
    CreateLocationUseCase,
    DeleteLocationUseCase,
    GetAllLocationsUseCase,
    GetLocationByIdUseCase,
)
from src.domain.use_cases.posts import (
    CreatePostUseCase,
    DeletePostUseCase,
    GetAllPostsUseCase,
    GetPostByIdUseCase,
    UpdatePostUseCase,
)
from src.domain.use_cases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
    UpdateUserUseCase,
)


async def get_user_by_id_use_case() -> GetUserByIdUseCase:
    return GetUserByIdUseCase()


async def get_all_users_use_case() -> GetAllUsersUseCase:
    return GetAllUsersUseCase()


async def create_user_use_case() -> CreateUserUseCase:
    return CreateUserUseCase()


async def update_user_use_case() -> UpdateUserUseCase:
    return UpdateUserUseCase()


async def delete_user_use_case() -> DeleteUserUseCase:
    return DeleteUserUseCase()


async def delete_location_use_case() -> DeleteLocationUseCase:
    return DeleteLocationUseCase()


async def create_location_use_case() -> CreateLocationUseCase:
    return CreateLocationUseCase()


async def get_all_locations_use_case() -> GetAllLocationsUseCase:
    return GetAllLocationsUseCase()


async def get_location_by_id_use_case() -> GetLocationByIdUseCase:
    return GetLocationByIdUseCase()


def authenticate_user_use_case() -> AuthenticateUseCase:
    return AuthenticateUseCase()


def create_access_token_use_case() -> CreateAccessTokenUseCase:
    return CreateAccessTokenUseCase()


async def get_all_categories_use_case() -> GetAllCategoriesUseCase:
    return GetAllCategoriesUseCase()


async def get_category_by_id_use_case() -> GetCategoryByIdUseCase:
    return GetCategoryByIdUseCase()


async def create_category_use_case() -> CreateCategoryUseCase:
    return CreateCategoryUseCase()


async def delete_category_use_case() -> DeleteCategoryUseCase:
    return DeleteCategoryUseCase()


async def get_all_posts_use_case() -> GetAllPostsUseCase:
    return GetAllPostsUseCase()


async def get_post_by_id_use_case() -> GetPostByIdUseCase:
    return GetPostByIdUseCase()


async def create_post_use_case() -> CreatePostUseCase:
    return CreatePostUseCase()


async def update_post_use_case() -> UpdatePostUseCase:
    return UpdatePostUseCase()


async def delete_post_use_case() -> DeletePostUseCase:
    return DeletePostUseCase()


async def get_all_comments_use_case() -> GetAllCommentsUseCase:
    return GetAllCommentsUseCase()


async def get_comment_by_id_use_case() -> GetCommentByIdUseCase:
    return GetCommentByIdUseCase()


async def get_comments_by_post_use_case() -> GetCommentsByPostUseCase:
    return GetCommentsByPostUseCase()


async def create_comment_use_case() -> CreateCommentUseCase:
    return CreateCommentUseCase()


async def delete_comment_use_case() -> DeleteCommentUseCase:
    return DeleteCommentUseCase()
