from pydantic import BaseModel, Field
from typing import Optional


class CreateUser(BaseModel):
    username: str = Field(..., max_length=50)
    firstname: str
    lastname: str
    age: int


class UpdateUser(BaseModel):
    firstname: str
    lastname: str
    age: int


class CreateTask(BaseModel):
    title: str
    content: str
    priority: int = 0


class UpdateTask(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    priority: Optional[int] = None
    completed: Optional[bool] = None
