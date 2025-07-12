from abc import ABC, abstractmethod
from mixins import SQLiteConnectionMixin
from typing import Any


class AbstractCurrencyRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_code(self, code) -> dict[str, Any] | None:
        pass


class SQLiteCurrencyRepository(
    SQLiteConnectionMixin,
    AbstractCurrencyRepository
):

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

    def find_by_code(self, code) -> dict[str, Any] | None:
        with self._create_connection() as conn:
            cursor = conn.cursor()
            query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.CODE} = ?'
            cursor.execute(query, (code,))
            row = cursor.fetchone()
            return dict(row) if row else None
