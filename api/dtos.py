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
    name: str = Field(min_length=1)
    code: str = Field(pattern=r'^[A-Z]{3}$')
    sign: str = Field(min_length=1)


class ExchangeRateReadDTO(BaseDTO):
    id: int
    base_currency: CurrencyReadDTO = Field(serialization_alias='baseCurrency')
    target_currency: CurrencyReadDTO = Field(serialization_alias='targetCurrency')
    rate: Decimal

    @field_serializer('rate')
    def serialize_rate(self, rate: Decimal, _info: FieldSerializationInfo) -> str:
        return rate.to_eng_string()


class ExchangeRateCreateDTO(BaseDTO):
    base_currency_code: str = Field(
        pattern=r'^[A-Z]{3}$', validation_alias='baseCurrencyCode'
    )
    target_currency_code: str = Field(
        pattern=r'^[A-Z]{3}$', validation_alias='targetCurrencyCode'
    )
    rate: Decimal = Field(max_digits=20, decimal_places=6, gt=0)


class ExchangeRateUpdateDTO(BaseDTO):
    rate: Decimal = Field(max_digits=20, decimal_places=6, gt=0)

class ExchangeCalculationDTO(BaseDTO):
    base_currency: CurrencyReadDTO = Field(serialization_alias='baseCurrency')
    target_currency: CurrencyReadDTO = Field(serialization_alias='targetCurrency')
    rate: Decimal
    amount: Decimal
    converted_amount: Decimal = Field(serialization_alias='convertedAmount')

    @field_serializer('rate', 'amount', 'converted_amount')
    def serialize_decimal(self, value: Decimal, _info: FieldSerializationInfo) -> str:
        return value.to_eng_string()


class ExchangeCalculationRequestDTO(BaseDTO):
    base_currency_code: str = Field(pattern=r'^[A-Z]{3}$', validation_alias='from')
    target_currency_code: str = Field(pattern=r'^[A-Z]{3}$', validation_alias='to')
    amount: Decimal =Field(max_digits=20, decimal_places=6, gt=0)

class ErrorDTO(BaseDTO):
    message: str
