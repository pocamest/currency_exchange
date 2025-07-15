import sqlite3

from data.interfaces import AbstractCurrencyDAO


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

    def insert(
        self, cursor: sqlite3.Cursor, code: str, full_name: str, sign: str
    ) -> int:
        query = f"""
                INSERT INTO {self.Table.NAME} (
                    {self.Table.CODE},
                    {self.Table.FULL_NAME},
                    {self.Table.SIGN}
                )
                VALUES (?, ?, ?)
            """
        try:
            cursor.execute(query, (code, full_name, sign))
            return cursor.lastrowid
        except sqlite3.IntegrityError:
            raise
