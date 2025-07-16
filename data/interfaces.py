from abc import ABC, abstractmethod
from typing import TypeVar

from domain import Currency

CursorType = TypeVar('CursorType')
RowType = TypeVar('RowType')
ConnectionType = TypeVar('ConnectionType')


class AbstractConnectionFactory[ConnectionType](ABC):
    @abstractmethod
    def create_connection(self) -> ConnectionType:
        pass


class AbstractCurrencyDAO[CursorType, RowType](ABC):
    @abstractmethod
    def fetch_all(self, cursor: CursorType) -> list[RowType]:
        pass

    @abstractmethod
    def fetch_by_code(self, cursor: CursorType, code: str) -> RowType | None:
        pass

    @abstractmethod
    def fetch_by_id(self, cursor: CursorType, id: int) -> RowType | None:
        pass

    @abstractmethod
    def insert(self, cursor: CursorType, code: str, full_name: str, sign: str) -> int:
        pass


class AbstractCurrencyRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[Currency]:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> Currency | None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> Currency | None:
        pass

    @abstractmethod
    def create(self, code: str, full_name: str, sign: str) -> Currency:
        pass
