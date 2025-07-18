from data import AbstractCurrencyRepository
from domain import Currency


class CurrencyController:
    def __init__(self, repo: AbstractCurrencyRepository):
        self._repo = repo

    def get_all(self) -> tuple[int, list[Currency]]:
        currencies = self._repo.find_all()
        return 200, currencies

    def create_currency(
        self, code: str, full_name: str, sign: str
    ) -> tuple[int, Currency]:
        created_currency = self._repo.create(code=code, full_name=full_name, sign=sign)
        return 201, created_currency
