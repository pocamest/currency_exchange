from typing import Any

from pydantic import ValidationError

from api.dtos import CurrencyCreateDTO, CurrencyReadDTO, ErrorDTO
from data import AbstractCurrencyRepository


class CurrencyController:
    def __init__(self, repo: AbstractCurrencyRepository):
        self._repo = repo

    def get_all(self) -> tuple[int, list[CurrencyReadDTO]]:
        currencies = self._repo.find_all()
        response_dto = [
            CurrencyReadDTO.model_validate(c) for c in currencies
        ]
        return 200, response_dto

    def create_currency(
        self, data: dict[str, Any]
    ) -> tuple[int, CurrencyReadDTO | ErrorDTO]:
        try:
            request_dto = CurrencyCreateDTO(**data)
        except ValidationError:
            return 400, ErrorDTO(
                message='Неверные или отсутствующие данные в теле запроса'
            )

        created_currency = self._repo.create(
            code=request_dto.code, full_name=request_dto.name, sign=request_dto.sign
        )
        response_dto = CurrencyReadDTO.model_validate(created_currency)
        return 201, response_dto
