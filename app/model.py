from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    id: str


class Song(BaseModel):
    _id: str = Field(...)
    title: str = Field(...)
    artists: List[dict] = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    song_file: str = Field(...)