from fastapi import APIRouter, Depends, HTTPException, status

from src.api.depends import (
    create_user_use_case,
    delete_user_use_case,
    get_all_users_use_case,
    get_user_by_id_use_case,
    update_user_use_case,
)
from src.core.exceptions.domain_exceptions import (
    PermissionDeniedException,
    UsernameIsOccupiedException,
    UserNotFoundByIdException,
    UserNotFoundByUsernameException,
    WrongPasswordException,
)
from src.domain.use_cases.users import (
    CreateUserUseCase,
    DeleteUserUseCase,
    GetAllUsersUseCase,
    GetUserByIdUseCase,
)
from src.domain.use_cases.users import UpdateUserUseCase
from src.schemas.users import (
    DeleteUserRequest,
    LoginUserResponse,
    RegisterUserRequest,
    UpdateUserRequest,
    UpdateUserResponse,
)
from src.services.auth import AuthService

router = APIRouter()


@router.get(
    "/users",
    response_model=list[LoginUserResponse],
    status_code=status.HTTP_200_OK,
)
async def get_all_users(
    use_case: GetAllUsersUseCase = Depends(get_all_users_use_case),
):
    return await use_case.execute()


@router.get(
    "/users/me",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_current_user_info(
    current_user: LoginUserResponse = Depends(
        AuthService.get_current_user
    ),
):
    return current_user


@router.get(
    "/users/{user_id}",
    response_model=LoginUserResponse,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
    current_user: LoginUserResponse = Depends(
        AuthService.get_current_user
    ),
):
    try:
        return await use_case.execute(user_id, current_user)
    except UserNotFoundByIdException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=exc.detail
        ) from exc


@router.post(
    "/users",
    response_model=LoginUserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user_data: RegisterUserRequest,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
):
    try:
        return await use_case.execute(user_data)
    except UsernameIsOccupiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        ) from exc


@router.delete(
    "/users/{username}", status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    username: str,
    delete_data: DeleteUserRequest,
    current_user: LoginUserResponse = Depends(
        AuthService.get_current_user
    ),
    use_case: DeleteUserUseCase = Depends(delete_user_use_case),
):
    try:
        await use_case.execute(
            username, current_user, delete_data.password
        )
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        ) from exc
    except PermissionDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        ) from exc
    return None


@router.put(
    "/users/{username}",
    response_model=UpdateUserResponse,
    status_code=status.HTTP_200_OK,
)
async def update_user(
    username: str,
    user_data: UpdateUserRequest,
    cur_user: LoginUserResponse = Depends(
        AuthService.get_current_user
    ),
    use_case: UpdateUserUseCase = Depends(update_user_use_case),
):
    try:
        return await use_case.execute(username, user_data, cur_user)
    except UserNotFoundByUsernameException as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=exc.detail,
        ) from exc
    except UsernameIsOccupiedException as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=exc.detail,
        ) from exc
    except WrongPasswordException as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=exc.detail,
        ) from exc
    except PermissionDeniedException as exc:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=exc.detail,
        ) from exc
