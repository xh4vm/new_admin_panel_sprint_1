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

        self.data = {Schema.genre : [], Schema.person : [], Schema.film_work : [],
            Schema.genre_film_work : [], Schema.person_film_work : [], }

    def load_movies(self, chunk : int = CHUNK) -> Iterator[type]:
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
            f'GROUP BY m.id '
            f'LIMIT {chunk};'
        )

        self.curs.execute(query)
        raw_objects : List[Dict[str, Any]] = self.curs.fetchmany(chunk)

        for raw_object in raw_objects:
            raw_object = dict_factory(self.curs, raw_object)

            self.data[Schema.genre].append(Genre(id=raw_object[f'{Schema.genre}_id'], 
                name=raw_object[f'{Schema.genre}_name'], description=raw_object[f'{Schema.genre}_description'],
                created_at=raw_object[f'{Schema.genre}_created_at'], updated_at=raw_object[f'{Schema.genre}_updated_at']))

            self.data[Schema.person].append(Person(id=raw_object[f'{Schema.person}_id'],
                full_name=raw_object[f'{Schema.person}_full_name'],
                created_at=raw_object[f'{Schema.person}_created_at'], updated_at=raw_object[f'{Schema.person}_updated_at']))

            self.data[Schema.film_work].append(FilmWork(id=raw_object[f'{Schema.film_work}_id'],
                title=raw_object[f'{Schema.film_work}_title'], description=raw_object[f'{Schema.film_work}_description'],
                creation_date=raw_object[f'{Schema.film_work}_creation_date'], file_path=raw_object[f'{Schema.film_work}_file_path'],
                rating=raw_object[f'{Schema.film_work}_rating'], type=raw_object[f'{Schema.film_work}_type'],
                created_at=raw_object[f'{Schema.film_work}_created_at'], updated_at=raw_object[f'{Schema.film_work}_updated_at']))

            self.data[Schema.genre_film_work].append(GenreFilmWork(id=raw_object[f'{Schema.genre_film_work}_id'], 
                film_work_id=raw_object[f'{Schema.genre_film_work}_film_work_id'], genre_id=raw_object[f'{Schema.genre_film_work}_genre_id'],
                created_at=raw_object[f'{Schema.genre_film_work}_created_at']))

            self.data[Schema.person_film_work].append(PersonFilmWork(id=raw_object[f'{Schema.person_film_work}_id'],
                film_work_id=raw_object[f'{Schema.person_film_work}_film_work_id'], 
                person_id=raw_object[f'{Schema.person_film_work}_person_id'], role=raw_object[f'{Schema.person_film_work}_role'], 
                created_at=raw_object[f'{Schema.person_film_work}_created_at']))

        print(self.data)


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
        
    # def load_movies(self, chunk : int = CHUNK) -> Iterator[FilmWork]:
    #     self.curs.execute(f'SELECT * FROM {Schema.film_work};')
    #     return self._convert_to_dataclass(_dataclass=FilmWork, chunk=chunk)

    def load_genre_movies(self, chunk : int = CHUNK) -> Iterator[GenreFilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.genre_film_work};')
        return self._convert_to_dataclass(_dataclass=GenreFilmWork, chunk=chunk)

    def load_person_movies(self, chunk : int = CHUNK) -> Iterator[PersonFilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.person_film_work};')
        return self._convert_to_dataclass(_dataclass=PersonFilmWork, chunk=chunk)
