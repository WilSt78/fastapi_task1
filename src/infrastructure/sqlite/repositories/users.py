from sqlalchemy.orm import Session
from typing import Optional
import logging
from sqlalchemy.exc import IntegrityError
from ...sqlite.models.userModel import User
from ....schemas.Users import UserRequest
from ....functions.verify_password import get_password_hash
from ....core.exceptions.database_exceptions import UsernameIsOccupied, EmailIsOccupied, UserNotFoundById, UserNotFoundByUsername, AlreadyExists
logger = logging.getLogger(__name__)

class UserRepository:
    def get_all(self, db: Session) -> list[User]:
        return db.query(User).all()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if not user:
                e = UserNotFoundByUsername(username=username)
                logger.error(e.get_detail())
                raise e
        return user

    def get_detail(self, db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            e = UserNotFoundById(id=user_id)
            logger.error(e.get_detail())
            raise e
        return user

    def create(self, db: Session, user_data: UserRequest) -> User:
    
        try:
            user = User(
            username=user_data.username,
            email=user_data.email,
            password=get_password_hash(user_data.password)
            )
            db.add(user)
            db.flush()
            return user
        except IntegrityError:
            raise AlreadyExists

    def update(self, db: Session, user_id: int,
               user_data: UserRequest) -> User:
        
        user = self.get_detail(db, user_id)

        if user_data.username != user.username:
            if db.query(User).filter(User.username ==
                                     user_data.username).first():
                e=UsernameIsOccupied(user_data.username)
                logger.error(e.get_detail())
                raise e

        if user_data.email != user.email:
            if db.query(User).filter(User.email == user_data.email).first():
                e= EmailIsOccupied(user_data.email)
                logger.error(e.get_detail())
                raise e

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
