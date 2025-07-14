from typing import Any

from .connection import DataBaseConnection
from .interfaces import AbstractCurrencyDAO, AbstractCurrencyRepository


class SQLiteCurrencyRepository(AbstractCurrencyRepository):
    def __init__(
        self, currency_dao: AbstractCurrencyDAO, connection: DataBaseConnection
    ):
        self.currency_dao = currency_dao
        self.connection = connection

    def find_all(self) -> list[dict[str, Any]]:
        with self.connection.create() as conn:
            cursor = conn.cursor()
            rows = self.currency_dao.fetch_all(cursor)
            return [dict(row) for row in rows]

    def find_by_code(self, code: str) -> dict[str, Any] | None:
        with self.connection.create() as conn:
            cursor = conn.cursor()
            row = self.currency_dao.fetch_by_code(cursor, code)
            return dict(row) if row else None

    def find_by_id(self, id: int) -> dict[str, Any] | None:
        with self.connection.create() as conn:
            cursor = conn.cursor()
            row = self.currency_dao.fetch_by_id(cursor, id)
            return dict(row) if row else None

    def create(self, code: str, full_name: str, sign: str) -> dict[str, Any]:
        with self.connection.create() as conn:
            cursor = conn.cursor()
            created_id = self.currency_dao.insert(cursor, code, full_name, sign)
            created_currency = self.currency_dao.fetch_by_id(cursor, created_id)
            if created_currency is None:
                raise Exception('Не удалось найти только что созданную валюту')
            return dict(created_currency)
