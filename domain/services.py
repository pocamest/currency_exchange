from domain.exceptions import NotFoundError
from domain.interfaces import AbstractCurrencyRepository, AbstractExcangeRateRepository
from domain.models import Currency, ExchangeRate


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
    def __init__(
        self,
        exchange_rate_repo: AbstractExcangeRateRepository,
        currency_repo: AbstractCurrencyRepository,
    ) -> None:
        self._exсhange_rate_repo = exchange_rate_repo
        self._currency_repo = currency_repo

    def get_all_full_exchange_rates(
        self,
    ) -> list[tuple[ExchangeRate, Currency, Currency]]:
        exchange_rates = self._exсhange_rate_repo.find_all()

        currency_ids = set()
        for exchange_rate in exchange_rates:
            currency_ids.add(exchange_rate.base_currency_id)
            currency_ids.add(exchange_rate.target_currency_id)

        currencies = self._currency_repo.find_by_ids(list(currency_ids))
        currencies_map = {c.id: c for c in currencies}

        result: list[tuple[ExchangeRate, Currency, Currency]] = []
        for exchange_rate in exchange_rates:
            base_currency = currencies_map.get(exchange_rate.base_currency_id)
            target_currency = currencies_map.get(exchange_rate.target_currency_id)
            if not base_currency or not target_currency:
                raise Exception('Не найдены валюты обменного курса')
            result.append((exchange_rate, base_currency, target_currency))
        return result

    def get_full_exchange_rate_by_currency_codes(
        self, base_code: str, target_code: str
    ) -> tuple[ExchangeRate, Currency, Currency]:
        base_currency = self._currency_repo.find_by_code(base_code)
        target_currency = self._currency_repo.find_by_code(target_code)
        if not base_currency or not target_currency:
            raise Exception('Не найдены валюты обменного курса')
        exchange_rate = self._exсhange_rate_repo.find_by_currency_ids(
            base_id=base_currency.id, target_id=target_currency.id
        )
        if not exchange_rate:
            raise NotFoundError(
                f'Обменный курс с кодами валют {base_code} и {target_code} не найден'
            )
        return exchange_rate, base_currency, target_currency
