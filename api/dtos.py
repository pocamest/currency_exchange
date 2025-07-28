from decimal import Decimal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    FieldSerializationInfo,
    field_serializer,
)


class BaseDTO(BaseModel):
    pass


class CurrencyReadDTO(BaseDTO):
    id: int
    name: str = Field(validation_alias='full_name')
    code: str
    sign: str

    model_config = ConfigDict(from_attributes=True)


class CurrencyCreateDTO(BaseDTO):
    name: str
    code: str
    sign: str


class ExchangeRateReadDTO(BaseDTO):
    id: int
    base_currency: CurrencyReadDTO = Field(serialization_alias='baseCurrency')
    target_currency: CurrencyReadDTO = Field(serialization_alias='targetCurrency')
    rate: Decimal

    @field_serializer('rate')
    def serialize(self, rate: Decimal, _info: FieldSerializationInfo) -> str:
        return str(rate)


class ErrorDTO(BaseDTO):
    message: str
