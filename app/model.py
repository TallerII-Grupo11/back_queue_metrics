from pydantic import BaseModel, Field
from typing import List


class User(BaseModel):
    id: str


class ArtistModel(BaseModel):
    artist_id: str = Field(...)
    artist_name: str = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)


class Song(BaseModel):
    _id: str = Field(...)
    title: str = Field(...)
    artists: List[ArtistModel] = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    song_file: str = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)

    def get_artists(self):
        list_artists = []
        for a in self.artists:
            list_artists.append({"artist_id": a["artist_id"]})
        return list_artists


class Playlist(BaseModel):
    _id: str = Field(...)
    title: str = Field(...)
    description: str = Field(...)
    songs: List[str] = []
    is_collaborative: bool = Field(...)
    owner_id: str = Field(...)

    def __getitem__(self, item):
        return getattr(self, item)


class Album(BaseModel):
    title: str = Field(...)
    artist: ArtistModel = Field(...)
    description: str = Field(...)
    genre: str = Field(...)
    image: str = Field(...)
    subscription: str = Field(...)
    songs: List[str] = []

    def __getitem__(self, item):
        return getattr(self, item)

    def get_artist(self):
        return {"artist_id": self.artist.artist_id}