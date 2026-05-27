from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    published: bool = Field(default=True)
    created: datetime = Field(default_factory=datetime.now)
