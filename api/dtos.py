from pydantic import BaseModel


class BaseDTO(BaseModel):
    pass

class CurrencyReadDTO(BaseDTO):
    id: int
    name: str
    code: str
    sign: str


class CurrencyCreateDTO(BaseDTO):
    name: str
    code: str
    sign: str


class ErrorDTO(BaseDTO):
    message: str
