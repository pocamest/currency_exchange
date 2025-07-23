from typing import Any

from pydantic import ValidationError

from api.dtos import CurrencyCreateDTO, CurrencyReadDTO, ErrorDTO
from data import AbstractCurrencyRepository


class CurrencyController:
    def __init__(self, currency_repo: AbstractCurrencyRepository):
        self._currency_repo = currency_repo

    def get_all(self) -> tuple[int, list[CurrencyReadDTO]]:
        currencies = self._currency_repo.find_all()
        response_dto = [
            CurrencyReadDTO.model_validate(c) for c in currencies
        ]
        return 200, response_dto

    def get_by_code(self, code: str) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        currency = self._currency_repo.find_by_code(code=code)
        if not currency:
            return 404, ErrorDTO(message='Валюта не найдена')
        response_dto = CurrencyReadDTO.model_validate(currency)
        return 200, response_dto

    def create_currency(
        self, body: dict[str, Any]
    ) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        try:
            request_dto = CurrencyCreateDTO(**body)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в теле запроса'
            )

        created_currency = self._currency_repo.create(
            code=request_dto.code, full_name=request_dto.name, sign=request_dto.sign
        )
        response_dto = CurrencyReadDTO.model_validate(created_currency)
        return 201, response_dto
