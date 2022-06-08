import datetime
import os
import pathlib
import sqlite3
from time import time
from typing import Any, Dict

import psycopg2

# from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from dotenv import load_dotenv

from sqlite_loader import SQLiteLoader
from postgres_saver import PostgresSaver


@contextmanager
def conn_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row

    yield conn

    conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_cursor: DictCursor) -> None:
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_cursor)
    sqlite_loader = SQLiteLoader(connection)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)

    data = sqlite_loader.load_movies()
    postgres_saver.save_all_data(data)


def get_postgresql_dsl() -> Dict[str, Any]:
    return {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
    }


def adapt_datetime(dt):
    # Get the datetime for the POSIX epoch.
    epoch = datetime.datetime.utcfromtimestamp(0.0)
    elapsedtime = dt - epoch
    # Calculate the number of milliseconds.
    seconds = float(elapsedtime.days)*24.*60.*60. + float(elapsedtime.seconds) + float(elapsedtime.microseconds)/1000000.0
    return seconds
def convert_datetime(tf):
    # Note: strange math is used to account for daylight savings time and 
    #    times in the Eastern (US) time zone (e.g. EDT)
    tf = float(tf)
    edt_adjustment = 6 * 60. * 60.
    if time.localtime(tf).tm_isdst:
        edt_adjustment = 5 * 60. * 60.
    return datetime.datetime.fromtimestamp(tf+edt_adjustment)


if __name__ == '__main__':
    load_dotenv()

    sqlite3.register_adapter(datetime.datetime, adapt_datetime)
    sqlite3.register_converter("datetime", convert_datetime)

    postgresql_dsl = get_postgresql_dsl()
    sqlite_path = os.environ.get('SQLITE_PATH')
    schema_file = os.path.join(pathlib.Path(__file__).parent.absolute(), 'schema.sql')

    with sqlite3.connect(
        sqlite_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
    ) as sqlite_conn, psycopg2.connect(
        **postgresql_dsl, cursor_factory=DictCursor
    ) as pg_conn, pg_conn.cursor() as pg_cursor:
        with open(schema_file, 'r') as schema_fd:
            pg_cursor.execute(schema_fd.read())

        load_from_sqlite(sqlite_conn, pg_cursor)
