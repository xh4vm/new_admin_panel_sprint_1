from typing import Iterator
from dataclasses import fields, astuple
from psycopg2.extras import DictCursor

from schema import Genre, Schema, FilmWork, Person, GenreFilmWork, PersonFilmWork, SCHEMA_NAME


class PostgresSaver:

    def __init__(self, pg_cursor : DictCursor):
        self.curs = pg_cursor

    def _multiple_insert(self, insert_query : str, data : Iterator[FilmWork]) -> None:
        self.curs.executemany(insert_query, (astuple(film_work) for film_work in data))

    def save_movies(self, data : Iterator[FilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.film_work}' 
            f'(title, description, creation_date, file_path, rating, type, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
        )

        self._multiple_insert(insert_query, data)

    def save_genres(self, data : Iterator[Genre]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre}' 
            f'(name, description, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s,%s)'
        )

        self._multiple_insert(insert_query, data)

    def save_persons(self, data : Iterator[Person]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person}' 
            f'(full_name, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s)'
        )

        self._multiple_insert(insert_query, data)

    def save_person_movies(self, data : Iterator[PersonFilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person_film_work}' 
            f'(film_work_id, person_id, role, created_at, id) '
            f'VALUES (%s,%s,%s,%s,%s)'
        )

        self._multiple_insert(insert_query, data)

    def save_genre_movies(self, data : Iterator[GenreFilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre_film_work}' 
            f'(film_work_id, genre_id, created_at, id) '
            f'VALUES (%s,%s,%s,%s)'
        )

        self._multiple_insert(insert_query, data)
