import sqlite3
from abc import ABC, abstractmethod
from typing import Any

from mixins import SQLiteConnectionMixin


class AbstractCurrencyRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def create(self, code: str, full_name: str, sign: str) -> dict[str, Any]:
        pass


class SQLiteCurrencyRepository(SQLiteConnectionMixin, AbstractCurrencyRepository):
    class Table:
        NAME = 'Currencies'

        ID = 'ID'
        CODE = 'Code'
        FULL_NAME = 'FullName'
        SIGN = 'Sign'

    def find_all(self) -> list[dict[str, Any]]:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM {self.Table.NAME}'
            cursor.execute(query)
            return [dict(row) for row in cursor.fetchall()]

    def find_by_code(self, code: str) -> dict[str, Any] | None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.CODE} = ?'
            cursor.execute(query, (code,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def find_by_id(self, id: int) -> dict[str, Any] | None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.ID} = ?'
            cursor.execute(query, (id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def create(self, code: str, full_name: str, sign: str) -> dict[str, Any]:
        query = f"""
                INSERT INTO {self.Table.NAME} (
                    {self.Table.CODE},
                    {self.Table.FULL_NAME},
                    {self.Table.SIGN}
                )
                VALUES (?, ?, ?)
            """
        with self._create_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(query, (code, full_name, sign))
                created_id = cursor.lastrowid
                created_currency = self.find_by_id(created_id)
                if created_currency is None:
                    raise Exception("Не удалось найти только что созданную валюту")
                return created_currency
            except sqlite3.IntegrityError:
                raise
