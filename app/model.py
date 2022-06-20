from pydantic import BaseModel


class User(BaseModel):
    id: str


class Task(BaseModel):
    id: str
    name: str