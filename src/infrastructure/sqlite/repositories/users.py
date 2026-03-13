from sqlalchemy.orm import Session
from fastapi import HTTPException
from typing import Optional
from ...sqlite.models.userModel import User
from ....schemas.Users import UserRequest


class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def get_detail(self, db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(
                status_code=404,
                detail='Пользователь не найден.')
        return user

    def create(self, db: Session, user_data: UserRequest) -> User:
        if db.query(User).filter(User.username == user_data.username).first():
            raise HTTPException(
                status_code=400,
                detail='Имя пользователя уже занято.')

        if db.query(User).filter(User.email == user_data.email).first():
            raise HTTPException(
                status_code=400,
                detail='Email уже используется.')

        user = User(
            username=user_data.username,
            email=user_data.email,
            password=user_data.password,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def update(self, db: Session, user_id: int,
               user_data: UserRequest) -> User:
        user = self.get_detail(db, user_id)

        if user_data.username != user.username:
            if db.query(User).filter(User.username ==
                                     user_data.username).first():
                raise HTTPException(
                    status_code=400,
                    detail='Имя пользователя уже занято.')

        if user_data.email != user.email:
            if db.query(User).filter(User.email == user_data.email).first():
                raise HTTPException(
                    status_code=400,
                    detail='Email уже используется.')

        user.username = user_data.username
        user.email = user_data.email
        user.password = user_data.password

        db.commit()
        db.refresh(user)
        return user

    def destroy(self, db: Session, user_id: int):
        user = self.get_detail(db, user_id)
        db.delete(user)
        db.commit()
