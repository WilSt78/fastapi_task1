from fastapi import status, HTTPException, APIRouter, Depends
from typing import List

from ..schemas.Users import UserResponse, UserRequest
from ..domain.use_cases.users import (
    GetAllUsersUseCase, 
    GetUserByUsernameUseCase, 
    GetUserByIdUseCase, 
    CreateUserUseCase,
    UpdateUserUseCase,
    DeleteUserUseCase,
    AlreadyOccupied
)
from .depends import (
    get_all_users_use_case, 
    get_user_by_id_use_case, 
    get_user_by_username_use_case,
    create_user_use_case,
    update_user_use_case,
    delete_user_use_case
)

from ..core.exceptions.domain_exceptions import (
    UserNotFoundByIdException, UserNotFoundByUsernameException
)
from ..core.exceptions.database_exceptions import EmailIsOccupied, UsernameIsOccupied, UserNotFoundById
router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[UserResponse])
async def get_all_users(
    use_case: GetAllUsersUseCase = Depends(get_all_users_use_case),
) -> List[UserResponse]:
    return await use_case.execute()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def register_user(
    user_data: UserRequest,
    use_case: CreateUserUseCase = Depends(create_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_data)
    except AlreadyOccupied as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=e.get_detail())


@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_id(
    user_id: int,
    use_case: GetUserByIdUseCase = Depends(get_user_by_id_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id)
    except UserNotFoundByIdException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=e.get_detail()
        )


@router.get("/by-username/{username}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def get_user_by_username(
    username: str,
    use_case: GetUserByUsernameUseCase = Depends(get_user_by_username_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(username)
    except UserNotFoundByUsernameException as e:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=e.get_detail()
        )



@router.put("/{user_id}", status_code=status.HTTP_200_OK, response_model=UserResponse)
async def update_user(
    user_id: int,
    user_data: UserRequest,
    use_case: UpdateUserUseCase = Depends(update_user_use_case),
) -> UserResponse:
    try:
        return await use_case.execute(user_id, user_data)
    except (UsernameIsOccupied, EmailIsOccupied) as e:
                 raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, 
            detail=e.get_detail()
        )
    except UserNotFoundById as e:
                raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=e.get_detail()
        )
         


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    use_case: DeleteUserUseCase = Depends(delete_user_use_case),
) -> None:
    await use_case.execute(user_id)
    return None