from typing import Any

from pydantic import ValidationError

from api.dtos import CurrencyCreateDTO, CurrencyReadDTO, ErrorDTO
from domain import CurrencyService, NotFoundError


class CurrencyController:
    def __init__(self, currency_service: CurrencyService):
        self._currency_service = currency_service

    def get_all_currencies(self) -> tuple[int, list[CurrencyReadDTO]]:
        currencies = self._currency_service.get_all_currencies()
        response_dto = [
            CurrencyReadDTO.model_validate(c) for c in currencies
        ]
        return 200, response_dto

    def get_currency_by_code(self, code: str) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        try:
            currency = self._currency_service.get_currency_by_code(code=code)
            response_dto = CurrencyReadDTO.model_validate(currency)
            return 200, response_dto
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

        created_currency = self._currency_service.create_currency(
            code=request_dto.code, full_name=request_dto.name, sign=request_dto.sign
        )
        response_dto = CurrencyReadDTO.model_validate(created_currency)
        return 201, response_dto
