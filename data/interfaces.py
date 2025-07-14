from abc import ABC, abstractmethod
from typing import Any


class AbstractCurrencyDAO(ABC):
    @abstractmethod
    def fetch_all(self, cursor: Any) -> list[Any]:
        pass

    @abstractmethod
    def fetch_by_code(self, cursor: Any, code: str) -> Any | None:
        pass

    @abstractmethod
    def fetch_by_id(self, cursor: Any, id: int) -> Any | None:
        pass

    @abstractmethod
    def insert(self, cursor: Any, code: str, full_name: str, sign: str) -> int:
        pass


class AbstractCurrencyRepository(ABC):
    @abstractmethod
    def find_all(self) -> list[dict[str, Any]]:
        pass

    @abstractmethod
    def find_by_code(self, code: str) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def find_by_id(self, id: int) -> dict[str, Any] | None:
        pass

    @abstractmethod
    def create(self, code: str, full_name: str, sign: str) -> dict[str, Any]:
        pass
