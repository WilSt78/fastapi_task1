from sqlalchemy.orm import Session
from typing import Optional
from ...infrastructure.sqlite.repositories.users import UserRepository
from ...schemas.Users import UserRequest, UserResponse


class UserUseCase:
    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository()

    def get_all_users(self) -> list[UserResponse]:
        users = self.repository.get_all(self.db)
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> UserResponse:
        user = self.repository.get_detail(self.db, user_id)
        return UserResponse.model_validate(user)

    def get_user_by_username(self, username: str) -> Optional[UserResponse]:
        user = self.repository.get_by_username(self.db, username)
        if user:
            return UserResponse.model_validate(user)
        return None

    def create_user(self, user_data: UserRequest) -> UserResponse:
        user = self.repository.create(self.db, user_data)
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int,
                    user_data: UserRequest) -> UserResponse:
        user = self.repository.update(self.db, user_id, user_data)
        return UserResponse.model_validate(user)

    def delete_user(self, user_id: int) -> dict:
        self.repository.destroy(self.db, user_id)
        return {"message": "Пользователь успешно удален"}
