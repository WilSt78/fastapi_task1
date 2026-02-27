from pydantic import BaseModel, Field, SecretStr, ConfigDict
from datetime import date, datetime
from typing import Optional

TEXT_LENGTH = 256
class Base(BaseModel):
    is_published : bool = Field(default=True,
                                 description= "Опубликовано")
    created_at : date = Field(description="Добавлено")
    
    model_config = ConfigDict(from_attributes=True) 

class Category(Base):
    title : str = Field(max_length=TEXT_LENGTH,
                         description="Заголовок")
    description : str = Field(description="Описание")
    slug : str
        
    model_config = ConfigDict(from_attributes=True)

class Location(Base):
    name : str = Field(max_length=TEXT_LENGTH,
                       description="Название места")
        
    model_config = ConfigDict(from_attributes=True)

class User(BaseModel):
    username : str = Field(description="Имя пользователя")
    email : str = Field(description="Email")
    password : SecretStr
        


class Post(Base):
    title : str = Field (max_length=TEXT_LENGTH)
    text : str
    pub_date : date = Field(default_factory=datetime.now)
    location : Optional[Location] = None
    author : User
    category : Optional[Category] = None
        
    model_config = ConfigDict(from_attributes=True)

class Comment(Base):
    text : str = Field(description="Текст комментария")
    post : Post = Field(description="Комментарий")
    created_at : date = Field(default_factory=datetime.now)
    author : User
        
    model_config = ConfigDict(from_attributes=True)