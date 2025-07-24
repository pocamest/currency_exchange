import sqlite3

from domain import AbstractConnectionFactory


class SQLiteConnectionFactory(AbstractConnectionFactory[sqlite3.Connection]):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        conn.row_factory = sqlite3.Row
        return conn
