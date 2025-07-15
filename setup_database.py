import sqlite3

from config import DATABASE_PATH


def create_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Currencies (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Code TEXT NOT NULL UNIQUE,
            FullName TEXT NOT NULL,
            Sign TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ExchangeRates (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            BaseCurrencyId INTEGER NOT NULL REFERENCES Currencies(ID),
            TargetCurrencyId INTEGER NOT NULL REFERENCES Currencies(ID),
            Rate REAL NOT NULL,
            UNIQUE (BaseCurrencyId, TargetCurrencyId)
        )
    """)


def insert_tables(cursor: sqlite3.Cursor) -> None:
    cursor.execute('SELECT COUNT(*) FROM Currencies')
    if cursor.fetchone()[0] == 0:
        currencies_data = [('USD', 'United States dollar', '$'), ('EUR', 'Euro', '€')]
        cursor.executemany(
            'INSERT INTO Currencies (Code, FullName, Sign) VALUES (?, ?, ?)',
            currencies_data,
        )

    cursor.execute('SELECT COUNT(*) FROM ExchangeRates')
    if cursor.fetchone()[0] == 0:
        try:
            cursor.execute("SELECT ID FROM Currencies WHERE Code = 'USD'")
            usd_id = cursor.fetchone()[0]
            cursor.execute("SELECT ID FROM Currencies WHERE Code = 'EUR'")
            eur_id = cursor.fetchone()[0]

            cursor.execute(
                'INSERT INTO ExchangeRates (BaseCurrencyId, TargetCurrencyId, Rate)'
                'VALUES (?, ?, ?)',
                (usd_id, eur_id, 0.99),
            )
        except (TypeError, IndexError):
            print('Ошибка: Не удалось найти ID для начальных валют.')


def setup() -> None:
    with sqlite3.connect(DATABASE_PATH) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()
        create_tables(cursor)
        insert_tables(cursor)


if __name__ == '__main__':
    setup()
