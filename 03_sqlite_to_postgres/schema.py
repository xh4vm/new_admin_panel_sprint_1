from datetime import date
import enum
from typing import Optional
import uuid 

from dataclasses import dataclass, field


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
    created: Optional[date] = field(default=None)
    modified: Optional[date] = field(default=None)

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
class FilmWork(FilmWorkBase, UUIDMixin, TimeStampedMixin):
    pass


@dataclass
class GenreBase:
    name : str
    description : str


@dataclass
class Genre(GenreBase, UUIDMixin, TimeStampedMixin):
    pass


@dataclass
class PersonBase:
    full_name : str


@dataclass
class Person(PersonBase, UUIDMixin, TimeStampedMixin):
    pass