import re
from typing import Any

from pydantic import ValidationError

from api.dtos import (
    CurrencyCreateDTO,
    CurrencyReadDTO,
    ErrorDTO,
    ExchangeCalculationDTO,
    ExchangeCalculationRequestDTO,
    ExchangeRateCreateDTO,
    ExchangeRateReadDTO,
    ExchangeRateUpdateDTO,
)
from application import CurrencyService, ExchangeRateService
from domain import ConflictError, NotFoundError


class CurrencyController:
    def __init__(self, currency_service: CurrencyService):
        self._currency_service = currency_service

    def get_all_currencies(self) -> tuple[int, list[CurrencyReadDTO]]:
        currencies_dto = self._currency_service.get_all_currencies()
        return 200, currencies_dto

    def get_currency_by_code(self, code: str) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        code_match = re.fullmatch(r'[A-Z]{3}', code)
        if not code_match:
            return 400, ErrorDTO(message=f'Код {code} некорректен')
        try:
            currency_dto = self._currency_service.get_currency_by_code(code=code)
            return 200, currency_dto
        except NotFoundError as e:
            return 404, ErrorDTO(message=str(e))

    def create_currency(
        self, body: dict[str, Any]
    ) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        try:
            request_dto = CurrencyCreateDTO(**body)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в теле запроса'
            )

        try:
            created_currency_dto = self._currency_service.create_currency(
                code=request_dto.code, full_name=request_dto.name, sign=request_dto.sign
            )
        except ConflictError as e:
            return 409, ErrorDTO(message=str(e))
        return 201, created_currency_dto


class ExchangeRateController:
    def __init__(self, exchange_rate_service: ExchangeRateService):
        self._exchange_rate_service = exchange_rate_service

    def get_all_exchange_rates(
        self,
    ) -> tuple[int, list[ExchangeRateReadDTO] | ErrorDTO]:
        try:
            exchange_rate_dtos = (
                self._exchange_rate_service.get_all_full_exchange_rates()
            )
            return 200, exchange_rate_dtos
        except Exception as e:
            return 500, ErrorDTO(message=str(e))

    def get_exchange_rate_by_currency_codes(
        self, currency_codes: str
    ) -> tuple[int, ExchangeRateReadDTO | ErrorDTO]:
        try:
            currency_codes_match = re.fullmatch(r'([A-Z]{3})([A-Z]{3})', currency_codes)
            if not currency_codes_match:
                return 400, ErrorDTO(
                    message='Коды некорректны или валют пары отсутствуют в адресе'
                )
            base_code = currency_codes_match.group(1)
            target_code = currency_codes_match.group(2)
            exchange_rate_dto = (
                self._exchange_rate_service.get_full_exchange_rate_by_currency_codes(
                    base_code=base_code, target_code=target_code
                )
            )
            return 200, exchange_rate_dto
        except NotFoundError as e:
            return 404, ErrorDTO(message=str(e))

    def create_exchange_rate(
        self, body: dict[str, Any]
    ) -> tuple[int, ExchangeRateReadDTO | ErrorDTO]:
        try:
            request_dto = ExchangeRateCreateDTO(**body)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в теле запроса'
            )
        try:
            created_exchange_rate_dto = (
                self._exchange_rate_service.create_exchange_rate(
                    base_currency_code=request_dto.base_currency_code,
                    target_currency_code=request_dto.target_currency_code,
                    rate=request_dto.rate,
                )
            )
        except NotFoundError as e:
            return 404, ErrorDTO(message=str(e))
        except ConflictError as e:
            return 409, ErrorDTO(message=str(e))
        return 201, created_exchange_rate_dto

    def update_exchange_rate(
        self, currency_codes: str, body: dict[str, Any]
    ) -> tuple[int, ExchangeRateReadDTO | ErrorDTO]:
        currency_codes_match = re.fullmatch(r'([A-Z]{3})([A-Z]{3})', currency_codes)
        if not currency_codes_match:
            return 400, ErrorDTO(
                message='Коды валют некорректны или отсутствуют в адресе'
            )
        base_code = currency_codes_match.group(1)
        target_code = currency_codes_match.group(2)
        try:
            request_dto = ExchangeRateUpdateDTO(**body)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в теле запроса'
            )
        try:
            updated_exchange_rate_dto = (
                self._exchange_rate_service.update_exchange_rate(
                    base_currency_code=base_code,
                    target_currency_code=target_code,
                    rate=request_dto.rate,
                )
            )
            return 200, updated_exchange_rate_dto
        except NotFoundError as e:
            return 404, ErrorDTO(message=str(e))

    def get_exchange_calculation(
        self, **query: Any
    ) -> tuple[int, ExchangeCalculationDTO | ErrorDTO]:
        try:
            query_dto = ExchangeCalculationRequestDTO.model_validate(query)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в параметрах запроса'
            )
        try:
            exchange_calculation_dto = self._exchange_rate_service.calculate_exchange(
                base_currency_code=query_dto.base_currency_code,
                target_currency_code=query_dto.target_currency_code,
                amount=query_dto.amount,
            )
            return 200, exchange_calculation_dto
        except NotFoundError as e:
            return 404, ErrorDTO(message=str(e))
