import sqlite3
from decimal import Decimal

from domain import AbstractConnectionFactory


def adapt_decimal(d: Decimal) -> str:
    return d.to_eng_string()


def convert_decimal(b: bytes) -> Decimal:
    return Decimal(b.decode())


sqlite3.register_adapter(Decimal, adapt_decimal)
sqlite3.register_converter('DECIMAL', convert_decimal)


class SQLiteConnectionFactory(AbstractConnectionFactory[sqlite3.Connection]):
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path

    def create_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(
            self.db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        conn.execute('PRAGMA foreign_keys = ON')
        conn.row_factory = sqlite3.Row
        return conn
