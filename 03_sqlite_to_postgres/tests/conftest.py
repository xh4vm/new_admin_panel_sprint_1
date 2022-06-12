import sqlite3
import psycopg2
import pytest
from dotenv import load_dotenv
from pathlib import Path
from psycopg2.extras import DictCursor
import os
from load_data import get_postgresql_dsl, conn_context


load_dotenv()

postgresql_dsl = get_postgresql_dsl()
sqlite_path = os.environ.get('SQLITE_PATH')


@pytest.fixture()
def sqlite_cursor():

    with conn_context(sqlite_path) as sqlite_conn:

        yield sqlite_conn.cursor()


@pytest.fixture()
def pg_cursor():

    with psycopg2.connect(**postgresql_dsl, cursor_factory=DictCursor) as pg_conn, pg_conn.cursor() as pg_cursor:

        yield pg_cursor
