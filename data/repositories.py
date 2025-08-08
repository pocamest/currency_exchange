import sqlite3
from decimal import Decimal

from domain import (
    AbstractConnectionFactory,
    AbstractCurrencyDAO,
    AbstractCurrencyRepository,
    AbstractExchangeRateDAO,
    AbstractExchangeRateRepository,
    Currency,
    ExchangeRate,
    ConflictError
)


class SQLiteCurrencyRepository(AbstractCurrencyRepository):
    def __init__(
        self,
        currency_dao: AbstractCurrencyDAO[sqlite3.Cursor, sqlite3.Row],
        connection_factory: AbstractConnectionFactory[sqlite3.Connection],
    ):
        self._currency_dao = currency_dao
        self._factory = connection_factory

    def find_all(self) -> list[Currency]:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            rows = self._currency_dao.fetch_all(cursor)
            return [Currency.model_validate(dict(row)) for row in rows]

    def find_by_code(self, code: str) -> Currency | None:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            row = self._currency_dao.fetch_by_code(cursor, code)
            return Currency.model_validate(dict(row)) if row else None

    def find_by_id(self, id: int) -> Currency | None:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            row = self._currency_dao.fetch_by_id(cursor, id)
            return Currency.model_validate(dict(row)) if row else None

    def find_by_ids(self, ids: list[int]) -> list[Currency]:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            rows = self._currency_dao.fetch_by_ids(cursor, ids)
            return [Currency.model_validate(dict(row)) for row in rows]

    def create(self, code: str, full_name: str, sign: str) -> Currency:
        try:
            with self._factory.create_connection() as conn:
                cursor = conn.cursor()
                created_id = self._currency_dao.insert(cursor, code, full_name, sign)
                created_currency = self._currency_dao.fetch_by_id(cursor, created_id)
                if created_currency is None:
                    raise Exception('Не удалось найти только что созданную валюту')
                return Currency.model_validate(dict(created_currency))
        except sqlite3.IntegrityError as e:
            raise ConflictError(
                f'Не удалось создать валюту с кодом {code}: '
                f'данные конфликтуют с уже существующими.'
            ) from e


class SQLiteExchangeRatesRepository(AbstractExchangeRateRepository):
    def __init__(
        self,
        exchange_rate_dao: AbstractExchangeRateDAO[sqlite3.Cursor, sqlite3.Row],
        connection_factory: AbstractConnectionFactory[sqlite3.Connection],
    ):
        self._exchange_rate_dao = exchange_rate_dao
        self._factory = connection_factory

    def find_all(self) -> list[ExchangeRate]:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            rows = self._exchange_rate_dao.fetch_all(cursor)
            return [ExchangeRate.model_validate(dict(row)) for row in rows]

    def find_by_currency_ids(self, base_id: int, target_id: int) -> ExchangeRate | None:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            row = self._exchange_rate_dao.fetch_by_currency_ids(
                cursor=cursor, base_id=base_id, target_id=target_id
            )
            return ExchangeRate.model_validate(dict(row)) if row else None

    def create(
        self, base_currency_id: int, target_currency_id: int, rate: Decimal
    ) -> ExchangeRate:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            created_id = self._exchange_rate_dao.insert(
                cursor=cursor,
                base_currency_id=base_currency_id,
                target_currency_id=target_currency_id,
                rate=rate,
            )
            created_exchange_rate = self._exchange_rate_dao.fetch_by_id(
                cursor=cursor, id=created_id
            )
            if not created_exchange_rate:
                raise Exception('Не удалось найти только что созданный обменный курс')
            return ExchangeRate.model_validate(dict(created_exchange_rate))

    def update(
        self, base_currency_id: int, target_currency_id: int, rate: Decimal
    ) -> bool:
        with self._factory.create_connection() as conn:
            cursor = conn.cursor()
            updated_rows_count = self._exchange_rate_dao.update(
                cursor=cursor,
                base_currency_id=base_currency_id,
                target_currency_id=target_currency_id,
                rate=rate
            )
            return updated_rows_count > 0
