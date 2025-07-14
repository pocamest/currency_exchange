import sqlite3
from abc import ABC, abstractmethod
from typing import Any


class DataBaseConnection(ABC):
    @abstractmethod
    def create(self) -> Any:
        pass


class SQLiteConnection:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def create(self) -> Any:
        conn = sqlite3.connect(self.db_path)
        conn.execute('PRAGMA foreign_keys = ON')
        conn.row_factory = sqlite3.Row
        return conn
