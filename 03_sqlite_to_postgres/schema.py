from datetime import date, datetime
import enum
from typing import Optional
import uuid 

from dataclasses import dataclass, field


SCHEMA_NAME = 'content'

class Schema:
    film_work = 'film_work'
    genre = 'genre'
    person = 'person'
    genre_film_work = 'genre_film_work'
    person_film_work = 'person_film_work'



class FilmWorkType(enum.Enum):
    tv_show = "TV Show"
    movie = "Movie"


@dataclass
class UUIDMixin:
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    class Meta:
        abstract = True


@dataclass
class TimeStampedMixin:
    created_at: Optional[date] = field(default=None)
    updated_at: Optional[date] = field(default=None)

    class Meta:
        abstract = True


@dataclass
class FilmWorkBase:
    title : str
    description : str
    file_path : str
    type: FilmWorkType
    creation_date: Optional[date] = field(default=None)
    rating: float = field(default=0.0)


@dataclass
class FilmWork(UUIDMixin, TimeStampedMixin, FilmWorkBase):
    pass


@dataclass
class GenreBase:
    name : str
    description : str


@dataclass
class Genre(UUIDMixin, TimeStampedMixin, GenreBase):
    pass


@dataclass
class GenreFilmWorkBase:
    film_work_id : uuid.UUID
    genre_id : uuid.UUID
    created_at : datetime


@dataclass
class GenreFilmWork(UUIDMixin, GenreFilmWorkBase):
    pass


@dataclass
class PersonBase:
    full_name : str


@dataclass
class Person(UUIDMixin, TimeStampedMixin, PersonBase):
    pass


@dataclass
class PersonFilmWorkBase:
    film_work_id : uuid.UUID
    person_id : uuid.UUID
    role : str
    created_at : datetime


@dataclass
class PersonFilmWork(UUIDMixin, PersonFilmWorkBase):
    pass
