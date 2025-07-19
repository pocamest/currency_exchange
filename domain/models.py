from pydantic import BaseModel, ConfigDict, Field


class Currency(BaseModel):
    id: int = Field(alias='ID')
    full_name: str = Field(alias='FullName')
    code: str = Field(alias='Code')
    sign: str = Field(alias='Sign')

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
