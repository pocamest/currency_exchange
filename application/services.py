from decimal import ROUND_HALF_UP, Decimal

from api.dtos import CurrencyReadDTO, ExchangeCalculationDTO, ExchangeRateReadDTO
from domain import (
    AbstractCurrencyRepository,
    AbstractExchangeRateRepository,
    Currency,
    ExchangeRate,
    NotFoundError,
    SystemError,
)


class CurrencyService:
    def __init__(self, currency_repo: AbstractCurrencyRepository):
        self._currency_repo = currency_repo

    def get_all_currencies(self) -> list[CurrencyReadDTO]:
        currency_models = self._currency_repo.find_all()
        return [CurrencyReadDTO.model_validate(c) for c in currency_models]

    def get_currency_by_code(self, code: str) -> CurrencyReadDTO:
        currency_model = self._currency_repo.find_by_code(code)
        if not currency_model:
            raise NotFoundError(f'Валюта с кодом {code} не найдена')
        return CurrencyReadDTO.model_validate(currency_model)

    def create_currency(self, code: str, full_name: str, sign: str) -> CurrencyReadDTO:
        created_currency_model = self._currency_repo.create(
            code=code, full_name=full_name, sign=sign
        )
        return CurrencyReadDTO.model_validate(created_currency_model)


class ExchangeRateService:
    def __init__(
        self,
        exchange_rate_repo: AbstractExchangeRateRepository,
        currency_repo: AbstractCurrencyRepository,
        cross_rate_base_code: str,
    ) -> None:
        self._exchange_rate_repo = exchange_rate_repo
        self._currency_repo = currency_repo
        self._cross_rate_base = cross_rate_base_code

    def _build_exchange_rate_dto(
        self,
        exchange_rate_model: ExchangeRate,
        base_currency_model: Currency,
        target_currency_model: Currency,
    ) -> ExchangeRateReadDTO:
        normalize_rate = exchange_rate_model.rate.quantize(
            Decimal('0.000001'), rounding=ROUND_HALF_UP
        )
        return ExchangeRateReadDTO(
            id=exchange_rate_model.id,
            base_currency=CurrencyReadDTO.model_validate(base_currency_model),
            target_currency=CurrencyReadDTO.model_validate(target_currency_model),
            rate=normalize_rate,
        )

    def _build_exchange_calculation_dto(
        self,
        base_currency_model: Currency,
        target_currency_model: Currency,
        rate: Decimal,
        amount: Decimal,
    ) -> ExchangeCalculationDTO:
        unrounded_amount = amount * rate
        converted_amount = unrounded_amount.quantize(
            Decimal('0.01'), rounding=ROUND_HALF_UP
        )
        normalized_rate = rate.quantize(Decimal('0.000001'), rounding=ROUND_HALF_UP)
        normalized_amount = amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        return ExchangeCalculationDTO(
            base_currency=CurrencyReadDTO.model_validate(base_currency_model),
            target_currency=CurrencyReadDTO.model_validate(target_currency_model),
            rate=normalized_rate,
            amount=normalized_amount,
            converted_amount=converted_amount,
        )

    def _find_currencies_by_codes(
        self, base_code: str, target_code: str
    ) -> tuple[Currency, Currency]:
        base_model = self._currency_repo.find_by_code(base_code)
        if not base_model:
            raise NotFoundError(f"Базовая валюта '{base_code}' не найдена")

        target_model = self._currency_repo.find_by_code(target_code)
        if not target_model:
            raise NotFoundError(f"Целевая валюта '{target_code}' не найдена")

        return base_model, target_model

    def _calculate_cross_rate(
        self, base_currency_id: int, target_currency_id: int
    ) -> Decimal | None:
        usd_currency = self._currency_repo.find_by_code(code=self._cross_rate_base)
        if not usd_currency:
            raise Exception('Ошибка конфигурации, валюта USD не найдена')

        exchange_rate_cross_to_base = self._exchange_rate_repo.find_by_currency_ids(
            base_id=usd_currency.id,
            target_id=base_currency_id,
        )
        exchange_rate_cross_to_target = self._exchange_rate_repo.find_by_currency_ids(
            base_id=usd_currency.id,
            target_id=target_currency_id,
        )

        if not exchange_rate_cross_to_base or not exchange_rate_cross_to_target:
            return None

        return 1 / exchange_rate_cross_to_base.rate * exchange_rate_cross_to_target.rate

    def get_all_full_exchange_rates(
        self,
    ) -> list[ExchangeRateReadDTO]:
        exchange_rate_models = self._exchange_rate_repo.find_all()

        base_ids = {e.base_currency_id for e in exchange_rate_models}
        target_ids = {e.target_currency_id for e in exchange_rate_models}
        currency_ids = base_ids | target_ids

        currency_models = self._currency_repo.find_by_ids(list(currency_ids))
        currencies_map = {c.id: c for c in currency_models}

        exchange_rate_dtos: list[ExchangeRateReadDTO] = []
        for exchange_rate in exchange_rate_models:
            base_currency = currencies_map.get(exchange_rate.base_currency_id)
            target_currency = currencies_map.get(exchange_rate.target_currency_id)
            if not base_currency or not target_currency:
                raise SystemError('Не найдены валюты обменного курса')
            exchange_rate_dtos.append(
                self._build_exchange_rate_dto(
                    exchange_rate, base_currency, target_currency
                )
            )
        return exchange_rate_dtos

    def get_full_exchange_rate_by_currency_codes(
        self, base_code: str, target_code: str
    ) -> ExchangeRateReadDTO:
        base_currency_model, target_currency_model = self._find_currencies_by_codes(
            base_code=base_code, target_code=target_code
        )
        exchange_rate_model = self._exchange_rate_repo.find_by_currency_ids(
            base_id=base_currency_model.id, target_id=target_currency_model.id
        )
        if not exchange_rate_model:
            raise NotFoundError(
                f'Обменный курс с кодами валют {base_code} и {target_code} не найден'
            )
        return self._build_exchange_rate_dto(
            exchange_rate_model, base_currency_model, target_currency_model
        )

    def create_exchange_rate(
        self, base_currency_code: str, target_currency_code: str, rate: Decimal
    ) -> ExchangeRateReadDTO:
        base_currency_model, target_currency_model = self._find_currencies_by_codes(
            base_code=base_currency_code, target_code=target_currency_code
        )
        exchange_rate_model = self._exchange_rate_repo.create(
            base_currency_id=base_currency_model.id,
            target_currency_id=target_currency_model.id,
            rate=rate,
        )
        return self._build_exchange_rate_dto(
            exchange_rate_model, base_currency_model, target_currency_model
        )

    def update_exchange_rate(
        self, base_currency_code: str, target_currency_code: str, rate: Decimal
    ) -> ExchangeRateReadDTO:
        base_currency_model, target_currency_model = self._find_currencies_by_codes(
            base_code=base_currency_code, target_code=target_currency_code
        )

        base_currency_id = base_currency_model.id
        target_currency_id = target_currency_model.id

        was_updated = self._exchange_rate_repo.update(
            base_currency_id=base_currency_id,
            target_currency_id=target_currency_id,
            rate=rate,
        )
        if not was_updated:
            raise NotFoundError(
                f'Обменный курс для пары '
                f'{base_currency_code}/{target_currency_code} не найден'
            )

        updated_exchange_rate_model = self._exchange_rate_repo.find_by_currency_ids(
            base_id=base_currency_id,
            target_id=target_currency_id,
        )
        if not updated_exchange_rate_model:
            raise SystemError('Не на удалось найти измененный обменный курс')
        return self._build_exchange_rate_dto(
            updated_exchange_rate_model, base_currency_model, target_currency_model
        )

    def calculate_exchange(
        self, base_currency_code: str, target_currency_code: str, amount: Decimal
    ) -> ExchangeCalculationDTO:
        base_currency_model, target_currency_model = self._find_currencies_by_codes(
            base_code=base_currency_code, target_code=target_currency_code
        )
        direct_rate = self._exchange_rate_repo.find_by_currency_ids(
            base_id=base_currency_model.id, target_id=target_currency_model.id
        )
        if direct_rate:
            rate = direct_rate.rate
            return self._build_exchange_calculation_dto(
                base_currency_model=base_currency_model,
                target_currency_model=target_currency_model,
                rate=rate,
                amount=amount,
            )

        reverse_rate = self._exchange_rate_repo.find_by_currency_ids(
            base_id=target_currency_model.id, target_id=base_currency_model.id
        )
        if reverse_rate:
            rate = 1 / reverse_rate.rate
            return self._build_exchange_calculation_dto(
                base_currency_model=base_currency_model,
                target_currency_model=target_currency_model,
                rate=rate,
                amount=amount,
            )

        cross_rate = self._calculate_cross_rate(
            base_currency_id=base_currency_model.id,
            target_currency_id=target_currency_model.id,
        )
        if cross_rate:
            return self._build_exchange_calculation_dto(
                base_currency_model=base_currency_model,
                target_currency_model=target_currency_model,
                rate=cross_rate,
                amount=amount,
            )

        raise NotFoundError(
            f'Обменный курс для валют '
            f'{base_currency_code}/{target_currency_code} не найден'
        )
