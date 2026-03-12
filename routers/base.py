from fastapi import status, HTTPException
from fastapi import APIRouter
from schemas.Users import UserResponse, UserRequest
from typing import Dict, List
from pydantic import SecretStr
from routers.is_there_user import is_there_user


router = APIRouter()
users: Dict[int, UserRequest] = {1: UserRequest(username="ya",
                                                email="ya@mail.ru",
                                                password=SecretStr("123"))}
user_id = 2


@router.get("/users", status_code=status.HTTP_200_OK,
            response_model=List[UserResponse])
async def get_all_users():
    response = []
    for id, user in users.items():
        response.append(
            UserResponse(id=id, username=user.username, email=user.email))
    return response


@router.post("/users/register", status_code=status.HTTP_201_CREATED,
             response_model=UserResponse)
async def register_user(username: str, email: str, password: str):
    global user_id
    if "@" not in email or "." not in email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат почты")
    for d in users.values():
        if d.email == email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с такой же почтой уже есть")
    user = UserRequest(
        username=username,
        email=email,
        password=SecretStr(password))
    users[user_id] = user
    user_id += 1
    return UserResponse(id=user_id - 1, username=username, email=email)


@router.get("/users/{id}", status_code=status.HTTP_200_OK,
            response_model=UserResponse)
async def get_user(id: int):
    if not is_there_user(id, users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден")
    user = users[id]
    return UserResponse(id=id, username=user.username, email=user.email)


@router.put("/users/{id}", status_code=status.HTTP_200_OK,
            response_model=UserResponse)
async def change_user(id: int, old_password: str, new_username: str,
                      new_email: str, new_password: str):
    if not is_there_user(id, users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден")
    if "@" not in new_email or "." not in new_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неверный формат почты")

    for uid, user in users.items():
        if uid != id and user.email == new_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Пользователь с таким email уже есть")

    user = users[id]
    if user.password.get_secret_value() != old_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль")

    user.username = new_username
    user.email = new_email
    user.password = SecretStr(new_password)
    return UserResponse(id=id, username=user.new_username,
                        email=user.new_email)


@router.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(id: int, password: str):
    if not is_there_user(id, users):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден")
    if users[id].password.get_secret_value() != password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный пароль")

    users.pop(id)
    return {"message": f"пользователь с id: {id} удален"}
