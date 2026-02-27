from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi import APIRouter, Response,status
from models import Post, User 
from typing import Dict
from pydantic import SecretStr


router= APIRouter()
users : Dict[int, User] = {1 : User(username="ya",
                                    email= "ya@mail.ru",
                                    password= SecretStr("123"))}
user_id = 1

@router.get("/users", status_code=status.HTTP_200_OK)
async def get_all_users():
    response=[]
    for id, user in users.items():
        response.append({"id" : id, "username" : user.username, "email" : user.email})
    return response

@router.post("/users/register",status_code=status.HTTP_200_OK)
async def register_user(username : str, email : str, password : str):
    global user_id
    if "@" not in email or "." not in email:
        raise HTTPException(status_code=400, detail="Неверный формат почты")
    for d in users.values():
        if d.email == email:
            raise HTTPException(status_code=400, detail="Пользователь с такой же почтой уже есть")
    user= User(username=username, email=email,password=SecretStr(password))
    users[user_id] = user
    user_id+=1
    return {
        "id": user_id - 1,
        "username": user.username,
        "email": user.email,
        "message": "Пользователь зарегистрирован"
    }

def is_there_user(id : int):
    if id not in users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Пользователь не найден"
        )
    return True

@router.get("/users/{id}", status_code=status.HTTP_200_OK)
async def get_user(id : int):
    if is_there_user(id):
        user = users[id]
        return {"name": user.username, "email": user.email}


@router.put("/users/{id}", status_code=status.HTTP_200_OK)
async def change_user(id : int,new_name : str,new_email : str,new_password : str):
    if is_there_user(id):
        if "@" not in new_email or "." not in new_email:
            raise HTTPException(status_code=400, detail="Неверный формат почты")
        user=users[id]
        user.username= new_name
        user.email=new_email
        user.password=new_password
    return {"message" : "Пользователь успешно изменен"}


@router.delete("/users/{id}", status_code=status.HTTP_200_OK)
async def delete_user(id : int, password : str):
    if is_there_user(id):
        if users[id].password.get_secret_value() == password:
            users.pop(id)
            return {"message" : "Пользователь удален"}
        else:
            return {"message" : "Неверный пароль"}
            



def create_app() ->FastAPI:
    app=FastAPI(root_path="/")
    app.add_middleware(
    CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True, 
        allow_methods=["*"], 
        allow_headers=["*"],
    )
    app.include_router(router,prefix="/base", tags=["Base APIs"])
    return app

