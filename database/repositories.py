from abc import ABC, abstractmethod
import sqlite3


class AbstractCurrencyRepository(ABC):
    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_code(self, code):
        pass


# подумать над названиями таблиц вынести ли х в переменные
class SQLiteCurrencyRepository(AbstractCurrencyRepository):
    def __init__(self, db_path: str):
        self.db_path = db_path

    def find_all(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM Currencies')
            return cursor.fetchall()

    def find_by_code(self, code):
        pass
