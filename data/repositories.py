import sqlite3

from data.interfaces import (
    AbstractConnectionFactory,
    AbstractCurrencyDAO,
    AbstractCurrencyRepository,
)
from domain import Currency


class SQLiteCurrencyRepository(AbstractCurrencyRepository):
    def __init__(
        self,
        currency_dao: AbstractCurrencyDAO[sqlite3.Cursor, sqlite3.Row],
        connection_factory: AbstractConnectionFactory[sqlite3.Connection],
    ):
        self.currency_dao = currency_dao
        self.factory = connection_factory

    def find_all(self) -> list[Currency]:
        with self.factory.create_connection() as conn:
            cursor = conn.cursor()
            rows = self.currency_dao.fetch_all(cursor)
            return [Currency(**row) for row in rows]

    def find_by_code(self, code: str) -> Currency | None:
        with self.factory.create_connection() as conn:
            cursor = conn.cursor()
            row = self.currency_dao.fetch_by_code(cursor, code)
            return Currency(**row) if row else None

    def find_by_id(self, id: int) -> Currency | None:
        with self.factory.create_connection() as conn:
            cursor = conn.cursor()
            row = self.currency_dao.fetch_by_id(cursor, id)
            return Currency(**row) if row else None

    def create(self, code: str, full_name: str, sign: str) -> Currency:
        with self.factory.create_connection() as conn:
            cursor = conn.cursor()
            created_id = self.currency_dao.insert(cursor, code, full_name, sign)
            created_currency = self.currency_dao.fetch_by_id(cursor, created_id)
            if created_currency is None:
                raise Exception('Не удалось найти только что созданную валюту')
            return Currency(**created_currency)
