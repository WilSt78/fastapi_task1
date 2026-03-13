from fastapi import status, HTTPException, APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from ..schemas.Users import UserResponse, UserRequest
from ..domain.use_cases.users import UserUseCase
from ..infrastructure.sqlite.database import get_db


router = APIRouter(prefix='/users', tags=['Пользователи'])


@router.get("/", status_code=status.HTTP_200_OK,
            response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    return use_case.get_all_users()


@router.post("/", status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
async def register_user(user_data: UserRequest, db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    return use_case.create_user(user_data)


@router.get("/{user_id}", status_code=status.HTTP_200_OK,
            response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    return use_case.get_user_by_id(user_id)


@router.get("/by-username/{username}", status_code=status.HTTP_200_OK,
            response_model=Optional[UserResponse])
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    return use_case.get_user_by_username(username)


@router.put("/{user_id}", status_code=status.HTTP_200_OK,
            response_model=UserResponse)
async def update_user(user_id: int, user_data: UserRequest,
                      db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    return use_case.update_user(user_id, user_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    use_case = UserUseCase(db)
    use_case.delete_user(user_id)
    return None
