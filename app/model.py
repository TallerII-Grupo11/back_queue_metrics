from pydantic import BaseModel


class User(BaseModel):
    id: str


class ArtistModel(BaseModel):
    artist_id: str = Field(...)
    artist_name: str = Field(...)


class Song(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    title: str = Field(...)
    artists: List[ArtistModel] = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    song_file: str = Field(...)