from dataclasses import dataclass
import sqlite3
from contextlib import contextmanager
from typing import Any, Dict, Iterator

from .schema import Genre, Schema, FilmWork


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


class SQLiteLoader:
    CHUNK = 20

    def __init__(self, connection: sqlite3.Connection) -> None:
        self.conn = connection
        self.curs = self.conn.cursor()

    def load_genres(self, chunk : int = CHUNK) -> Iterator[Genre]:
        self.curs.execute(f'SELECT * FROM {Schema.genre};')

    def load_movies(self, chunk : int = CHUNK) -> Iterator[FilmWork]:
        self.curs.execute(f'SELECT * FROM {Schema.film_work};')
        
