from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Currency(BaseModel):
    id: int = Field(alias='ID')
    full_name: str = Field(alias='FullName')
    code: str = Field(alias='Code')
    sign: str = Field(alias='Sign')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class ExchangeRates(BaseModel):
    id: int = Field(alias='ID')
    base_currency_id: int = Field(alias='BaseCurrencyId')
    target_currency_id: int = Field(alias='TargetCurrencyId')
    rate: Decimal = Field(alias='Rate')

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
