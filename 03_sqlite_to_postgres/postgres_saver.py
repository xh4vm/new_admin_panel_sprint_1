from typing import Any, Callable, Dict, Iterator, List, Optional, Tuple
import logging

from psycopg2.extras import DictCursor, execute_values

from schema import Genre, Schema, FilmWork, Person, GenreFilmWork, PersonFilmWork, SCHEMA_NAME


class PostgresSaver:

    def __init__(self, pg_cursor: DictCursor, chunk_size: int = 20):
        self.curs = pg_cursor
        self.loaded_data = {
            Schema.genre: [],
            Schema.person: [],
            Schema.film_work: [],
            Schema.genre_film_work: [],
            Schema.person_film_work: [],
        }
        self.chunk_size = chunk_size
    
        logging.root.setLevel(logging.NOTSET)
        logging.basicConfig(level=logging.NOTSET)
        self.logger = logging.getLogger(__name__)

    def _multiple_insert(self, insert_query: str, data: List[Tuple[Any]]) -> None:
        execute_values(self.curs, insert_query, data)

    def _save_movies(self, data: Iterator[FilmWork]) -> None:
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.film_work}'
            f'(title, description, creation_date, file_path, rating, type, created_at, updated_at, id) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query,
            (
                (
                    elem.title,
                    elem.description,
                    elem.creation_date,
                    elem.file_path,
                    elem.rating,
                    elem.type,
                    elem.created_at,
                    elem.updated_at,
                    elem.id,
                )
                for elem in data
            ),
        )

        self.logger.debug(f'Success multiple insert movies ({len(data)} objects)')

    def _save_genres(self, data: Iterator[Genre]) -> None:
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre}'
            f'(name, description, created_at, updated_at, id) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query, ((elem.name, elem.description, elem.created_at, elem.updated_at, elem.id,) for elem in data)
        )

        self.logger.debug(f'Success multiple insert genres ({len(data)} objects)')

    def _save_persons(self, data: Iterator[Person]) -> None:
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person}'
            f'(full_name, created_at, updated_at, id) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query, ((elem.full_name, elem.created_at, elem.updated_at, elem.id,) for elem in data)
        )

        self.logger.debug(f'Success multiple insert persons ({len(data)} objects)')

    def _save_person_movies(self, data: Iterator[PersonFilmWork]) -> None:
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.person_film_work}'
            f'(film_work_id, person_id, role, created_at, id) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query, ((elem.film_work_id, elem.person_id, elem.role, elem.created_at, elem.id,) for elem in data)
        )
        
        self.logger.debug(f'Success multiple insert person_movies ({len(data)} objects)')

    def _save_genre_movies(self, data: Iterator[GenreFilmWork]) -> None:
        insert_query: str = (
            f'INSERT INTO {SCHEMA_NAME}.{Schema.genre_film_work}'
            f'(film_work_id, genre_id, created_at, id) '
            f'VALUES %s ON CONFLICT (id) DO NOTHING'
        )

        self._multiple_insert(
            insert_query, ((elem.film_work_id, elem.genre_id, elem.created_at, elem.id,) for elem in data)
        )

        self.logger.debug(f'Success multiple insert genre_movies ({len(data)} objects)')

    def _stack_or_flush(self, schema_name: str, data: Optional[type], callback: Callable[[Iterator[type]], None], is_last: bool):
        if data is not None:
            self.loaded_data[schema_name].append(data)

        if len(self.loaded_data[schema_name]) == self.chunk_size or is_last:
            callback(self.loaded_data[schema_name])
            self.loaded_data.update({schema_name: []})
            self.logger.debug(f'Chunk from {schema_name} schema has been flushed!')

    def _stack_or_flush_all_data(self, obj: Dict[str, type], is_last: bool = False) -> None:
        try:
            self._stack_or_flush(schema_name=Schema.genre, data=obj[Schema.genre], callback=self._save_genres, is_last=is_last)
            self._stack_or_flush(schema_name=Schema.person, data=obj[Schema.person], callback=self._save_persons, is_last=is_last)
            self._stack_or_flush(schema_name=Schema.film_work, data=obj[Schema.film_work], callback=self._save_movies, is_last=is_last)
            self._stack_or_flush(
                schema_name=Schema.genre_film_work, data=obj[Schema.genre_film_work], callback=self._save_genre_movies, is_last=is_last
            )
            self._stack_or_flush(
                schema_name=Schema.person_film_work,
                data=obj[Schema.person_film_work],
                callback=self._save_person_movies,
                is_last=is_last
            )

            self.curs.execute('COMMIT;')
        
        except Exception as err:
            self.curs.execute('ROLLBACK;')
            
            self.logger.error(f'Error stack or flush data! Message: {err}')

            raise err

    def save_all_data(self, data: Iterator[Dict[str, type]]) -> None:
        last_obj = {Schema.genre: None,
            Schema.person: None,
            Schema.film_work: None,
            Schema.genre_film_work: None,
            Schema.person_film_work: None}

        self.logger.info(f'Start saving all data to PostgreSQL database instance.')

        for obj in data:
            self._stack_or_flush_all_data(obj)

        self._stack_or_flush_all_data(obj=last_obj, is_last=True)

        self.logger.info(f'Success finish saving all data to PostgreSQL database instance.')
