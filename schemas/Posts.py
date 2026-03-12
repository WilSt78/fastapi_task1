from .Base import Base
from .Locations import Location
from .Users import UserRequest
from .Categories import Category
from pydantic import Field
from datetime import date, datetime
from typing import Optional


TEXT_LENGTH = 256


class Post(Base):
    title: str = Field(max_length=TEXT_LENGTH)
    text: str
    pub_date: date = Field(default_factory=datetime.now)
    location: Optional[Location] = None
    author: UserRequest
    category: Optional[Category] = None
