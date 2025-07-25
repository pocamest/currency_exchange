from domain.exceptions import NotFoundError
from domain.interfaces import AbstractCurrencyRepository, AbstractExcangeRateRepository
from domain.models import Currency


class CurrencyService:
    def __init__(self, currency_repo: AbstractCurrencyRepository):
        self._currency_repo = currency_repo

    def get_all_currencies(self) -> list[Currency]:
        return self._currency_repo.find_all()

    def get_currency_by_code(self, code: str) -> Currency:
        currency = self._currency_repo.find_by_code(code)
        if not currency:
            raise NotFoundError(f'Валюта с кодом {code} не найдена')
        return currency

    def create_currency(self, code: str, full_name: str, sign: str) -> Currency:
        return self._currency_repo.create(code=code, full_name=full_name, sign=sign)


class ExchangeRateService:
    def __init__(self, exchange_rate_repo: AbstractExcangeRateRepository):
        self._exhange_rate_repo = exchange_rate_repo
