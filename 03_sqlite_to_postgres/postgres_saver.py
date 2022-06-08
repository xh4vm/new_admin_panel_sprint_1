from typing import Any, Dict, Iterator, List
from dataclasses import fields, astuple
from psycopg2.extras import DictCursor

from schema import Genre, Schema, FilmWork, Person, GenreFilmWork, PersonFilmWork, SCHEMA_NAME


class PostgresSaver:
    CHUNK = 20

    def __init__(self, pg_cursor : DictCursor):
        self.curs = pg_cursor
        self.loaded_data = {Schema.genre : [], Schema.person : [], Schema.film_work : [],
            Schema.genre_film_work : [], Schema.person_film_work : [], }

    def _multiple_insert(self, insert_query : str, data : Iterator[type]) -> None:
        self.curs.executemany(insert_query, (astuple(element) for element in data))

    def _save_movies(self, data : Iterator[FilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.film_work}' 
            f'(title, description, creation_date, file_path, rating, type, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
        )

        self._multiple_insert(insert_query, data)

    def _save_genres(self, data : Iterator[Genre]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre}' 
            f'(name, description, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
        )

        self._multiple_insert(insert_query, data)

    def _save_persons(self, data : Iterator[Person]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person}' 
            f'(full_name, created_at, updated_at, id) '
            f'VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING'
        )

        self._multiple_insert(insert_query, data)

    def _save_person_movies(self, data : Iterator[PersonFilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person_film_work}' 
            f'(film_work_id, person_id, role, created_at, id) '
            f'VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING'
        )

        self._multiple_insert(insert_query, data)

    def _save_genre_movies(self, data : Iterator[GenreFilmWork]) -> None:
        insert_query : str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre_film_work}' 
            f'(film_work_id, genre_id, created_at, id) '
            f'VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING'
        )

        self._multiple_insert(insert_query, data)

    def _stack_or_flush(self, schema_name : str, data : type, callback):
        if data is not None:
            self.loaded_data[schema_name].append(data)

        if len(self.loaded_data[schema_name]) == self.CHUNK:
            callback(self.loaded_data[schema_name])
            self.loaded_data.update({schema_name: []})

    def save_all_data(self, data: Iterator[Dict[str, type]]) -> None:
        
        for obj in data:
            
            self._stack_or_flush(schema_name=Schema.genre, data=obj[Schema.genre], callback=self._save_genres)
            self._stack_or_flush(schema_name=Schema.person, data=obj[Schema.person], callback=self._save_persons)
            self._stack_or_flush(schema_name=Schema.film_work, data=obj[Schema.film_work], callback=self._save_movies)
            self._stack_or_flush(schema_name=Schema.genre_film_work, data=obj[Schema.genre_film_work], callback=self._save_genre_movies)
            self._stack_or_flush(schema_name=Schema.person_film_work, data=obj[Schema.person_film_work], callback=self._save_person_movies)
