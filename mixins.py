import sqlite3


class SQLiteConnectionMixin:
    def __init__(self, db_path):
        self.db_path = db_path

    def _create_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn
