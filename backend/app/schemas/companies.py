from pydantic import BaseModel, Field


class CompanyOut(BaseModel):
    id: str
    ticker: str
    name: str
    exchange: str | None = None


class CompanyCreate(BaseModel):
    ticker: str = Field(min_length=1, max_length=16)
    name: str = Field(min_length=1, max_length=200)
    exchange: str | None = Field(default=None, max_length=32)
