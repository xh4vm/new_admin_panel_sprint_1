from dataclasses import is_dataclass
from datetime import datetime
import sqlite3
from typing import Any, Dict, Iterator, List
import uuid
from dateutil.parser import parse

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

    def load_movies(self, chunk: int = CHUNK) -> Iterator[type]:
        query = (
            f'SELECT m.id as {Schema.film_work}_id, m.title as {Schema.film_work}_title, m.description as {Schema.film_work}_description, '
            f'm.creation_date as {Schema.film_work}_creation_date, m.file_path as {Schema.film_work}_file_path, m.rating as {Schema.film_work}_rating, '
            f'm.type as {Schema.film_work}_type, m.created_at as {Schema.film_work}_created_at, m.updated_at as {Schema.film_work}_updated_at, '
            f'g.id as {Schema.genre}_id, g.name as {Schema.genre}_name, '
            f'g.description as {Schema.genre}_description, g.created_at as {Schema.genre}_created_at, g.updated_at as {Schema.genre}_updated_at, '
            f'p.id as {Schema.person}_id, p.full_name as {Schema.person}_full_name, p.created_at as {Schema.person}_created_at, '
            f'p.updated_at as {Schema.person}_updated_at, '
            f'mg.id as {Schema.genre_film_work}_id, mg.film_work_id as {Schema.genre_film_work}_film_work_id, '
            f'mg.genre_id as {Schema.genre_film_work}_genre_id, mg.created_at as {Schema.genre_film_work}_created_at, '
            f'mp.id as {Schema.person_film_work}_id, mp.film_work_id as {Schema.person_film_work}_film_work_id, '
            f'mp.person_id as {Schema.person_film_work}_person_id, mp.created_at as {Schema.person_film_work}_created_at, '
            f'mp.role as {Schema.person_film_work}_role '
            f'FROM film_work m '
            f'LEFT JOIN genre_film_work mg ON mg.film_work_id = m.id '
            f'LEFT JOIN genre g ON mg.genre_id = g.id '
            f'LEFT JOIN person_film_work mp ON mp.film_work_id = m.id '
            f'LEFT JOIN person p ON mp.person_id = p.id '
            f'GROUP BY m.id;'
        )
        data = {
            Schema.genre: None,
            Schema.person: None,
            Schema.film_work: None,
            Schema.genre_film_work: None,
            Schema.person_film_work: None,
        }
        raw_objects = None
        self.curs.execute(query)

        while raw_objects != []:
            raw_objects: List[Dict[str, Any]] = self.curs.fetchmany(chunk)

            for raw_object in raw_objects:
                raw_object = dict_factory(self.curs, raw_object)

                data[Schema.genre] = Genre(
                    id=uuid.UUID(raw_object[f'{Schema.genre}_id']),
                    name=raw_object[f'{Schema.genre}_name'],
                    description=raw_object[f'{Schema.genre}_description'],
                    created_at=parse(raw_object[f'{Schema.genre}_created_at']),
                    updated_at=parse(raw_object[f'{Schema.genre}_updated_at']),
                )

                data[Schema.person] = Person(
                    id=uuid.UUID(raw_object[f'{Schema.person}_id']),
                    full_name=raw_object[f'{Schema.person}_full_name'],
                    created_at=parse(raw_object[f'{Schema.person}_created_at']),
                    updated_at=parse(raw_object[f'{Schema.person}_updated_at']),
                )

                data[Schema.film_work] = FilmWork(
                    id=uuid.UUID(raw_object[f'{Schema.film_work}_id']),
                    title=raw_object[f'{Schema.film_work}_title'],
                    description=raw_object[f'{Schema.film_work}_description'],
                    creation_date=raw_object[f'{Schema.film_work}_creation_date'],
                    file_path=raw_object[f'{Schema.film_work}_file_path'],
                    rating=raw_object[f'{Schema.film_work}_rating'],
                    type=raw_object[f'{Schema.film_work}_type'],
                    created_at=parse(raw_object[f'{Schema.film_work}_created_at']),
                    updated_at=parse(raw_object[f'{Schema.film_work}_updated_at']),
                )

                data[Schema.genre_film_work] = GenreFilmWork(
                    id=uuid.UUID(raw_object[f'{Schema.genre_film_work}_id']),
                    film_work_id=uuid.UUID(raw_object[f'{Schema.genre_film_work}_film_work_id']),
                    genre_id=uuid.UUID(raw_object[f'{Schema.genre_film_work}_genre_id']),
                    created_at=parse(raw_object[f'{Schema.genre_film_work}_created_at']),
                )

                data[Schema.person_film_work] = PersonFilmWork(
                    id=uuid.UUID(raw_object[f'{Schema.person_film_work}_id']),
                    film_work_id=uuid.UUID(raw_object[f'{Schema.person_film_work}_film_work_id']),
                    person_id=uuid.UUID(raw_object[f'{Schema.person_film_work}_person_id']),
                    role=raw_object[f'{Schema.person_film_work}_role'],
                    created_at=parse(raw_object[f'{Schema.person_film_work}_created_at']),
                )

                yield data
