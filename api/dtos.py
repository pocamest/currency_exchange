from pydantic import BaseModel, ConfigDict, Field


class BaseDTO(BaseModel):
    pass

class CurrencyReadDTO(BaseDTO):
    id: int
    name: str = Field(validation_alias='full_name')
    code: str
    sign: str

    model_config = ConfigDict(
        from_attributes=True
    )


class CurrencyCreateDTO(BaseDTO):
    name: str
    code: str
    sign: str


class ExchangeRateReadDTO(BaseDTO):
    id: int
    base_currency: CurrencyReadDTO = Field(alias='baseCurrency')
    target_currency: CurrencyReadDTO = Field(alias='targetCurrency')


class ErrorDTO(BaseDTO):
    message: str
