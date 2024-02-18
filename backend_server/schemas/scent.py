import datetime as dt

from pydantic import BaseModel, ConfigDict, Field


class ScentApiCreate(BaseModel):
    index: list[int]
    temperature: list[float]
    humidity: list[float]
    pressure: list[float]
    gas_value: list[float]


class ScentApiCreateResponse(BaseModel):
    scent_id: int


class ScentSingleMeasurement(BaseModel):
    index: int
    temperature: float
    humidity: float
    pressure: float
    gas_value: float


class ScentDBCreate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    sensored_at: dt.datetime
    temperature: float
    humidity: float
    pressure: float
    gas_feature: list[float] = Field(..., min_items=19, max_items=19)


class ScentApiRead(ScentDBCreate):
    id: int
