import sqlite3

from domain import AbstractCurrencyDAO, AbstractExchangeRateDAO


class SQLiteCurrencyDAO(AbstractCurrencyDAO[sqlite3.Cursor, sqlite3.Row]):
    class Table:
        NAME = 'Currencies'

        ID = 'ID'
        CODE = 'Code'
        FULL_NAME = 'FullName'
        SIGN = 'Sign'

    def fetch_all(self, cursor: sqlite3.Cursor) -> list[sqlite3.Row]:
        query = f'SELECT * FROM {self.Table.NAME}'
        cursor.execute(query)
        return cursor.fetchall()

    def fetch_by_code(self, cursor: sqlite3.Cursor, code: str) -> sqlite3.Row | None:
        query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.CODE} = ?'
        cursor.execute(query, (code,))
        row = cursor.fetchone()
        return row if row else None

    def fetch_by_id(self, cursor: sqlite3.Cursor, id: int) -> sqlite3.Row | None:
        query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.ID} = ?'
        cursor.execute(query, (id,))
        row = cursor.fetchone()
        return row if row else None

    def fetch_by_ids(self, cursor: sqlite3.Cursor, ids: list[int]) -> list[sqlite3.Row]:
        if not ids:
            return []
        pattern = ', '.join('?' for _ in ids)
        query = f'SELECT * FROM {self.Table.NAME} WHERE {self.Table.ID} IN ({pattern})'
        cursor.execute(query, ids)
        return cursor.fetchall()

    def insert(
        self, cursor: sqlite3.Cursor, code: str, full_name: str, sign: str
    ) -> int:
        query = f'''
            INSERT INTO {self.Table.NAME} (
                {self.Table.CODE},
                {self.Table.FULL_NAME},
                {self.Table.SIGN}
            )
            VALUES (?, ?, ?)
        '''
        cursor.execute(query, (code, full_name, sign))
        id = cursor.lastrowid
        if not id:
            raise sqlite3.OperationalError(
                'Не удалось получить ID после вставки записи.'
            )
        return id


class SQLiteExchangeRatesDAO(AbstractExchangeRateDAO[sqlite3.Cursor, sqlite3.Row]):
    class Table:
        NAME = 'ExchangeRates'

        ID = 'ID'
        BASE_CURRENCY_ID = 'BaseCurrencyId'
        TARGET_CURRENCY_ID = 'TargetCurrencyId'
        RATE = 'Rate'

    def fetch_all(self, cursor: sqlite3.Cursor) -> list[sqlite3.Row]:
        query = f'SELECT * FROM {self.Table.NAME}'
        cursor.execute(query)
        return cursor.fetchall()

    def fetch_by_currency_ids(
        self, cursor: sqlite3.Cursor, base_id: int, target_id: int
    ) -> sqlite3.Row | None:
        query = f"""
            SELECT * FROM {self.Table.NAME}
            WHERE {self.Table.BASE_CURRENCY_ID} = ?
            AND {self.Table.TARGET_CURRENCY_ID} = ?
        """
        cursor.execute(query, (base_id, target_id))
        row = cursor.fetchone()
        return row if row else None
