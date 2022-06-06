from dataclasses import is_dataclass
import sqlite3
from typing import Any, Dict, Iterator, List

from schema import Genre, Schema, FilmWork, Person, GenreFilmWork, PersonFilmWork


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class SQLiteLoader:
    CHUNK = 20

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self.curs = self.conn.cursor()

    def _convert_to_dataclass(self, _dataclass : type, chunk : int) -> Iterator[type]:
        
        if not is_dataclass(_dataclass):
            raise TypeError(f'Error dataclass type: {_dataclass}')
        
        raw_objects : List[Dict[str, Any]] = self.curs.fetchmany(chunk)

        for raw_object in raw_objects:
            yield _dataclass(**dict_factory(self.curs, raw_object))

    def load_genres(self, chunk : int = CHUNK) -> Iterator[Genre]:
        self.curs.execute(f'SELECT * FROM {Schema.genre};')
        return self._convert_to_dataclass(_dataclass=Genre, chunk=chunk)

    def load_persons(self, chunk : int = CHUNK) -> Iterator[Person]:
        self.curs.execute(f'SELECT * FROM {Schema.person};')
        return self._convert_to_dataclass(_dataclass=Person, chunk=chunk)
        
    def load_movies(self, chunk : int = CHUNK) -> Iterator[FilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.film_work};')
        return self._convert_to_dataclass(_dataclass=FilmWork, chunk=chunk)

    def load_genre_movies(self, chunk : int = CHUNK) -> Iterator[GenreFilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.genre_film_work};')
        return self._convert_to_dataclass(_dataclass=GenreFilmWork, chunk=chunk)

    def load_person_movies(self, chunk : int = CHUNK) -> Iterator[PersonFilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.person_film_work};')
        return self._convert_to_dataclass(_dataclass=PersonFilmWork, chunk=chunk)
