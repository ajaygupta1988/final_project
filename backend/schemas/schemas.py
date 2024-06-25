from typing import List, Dict, Optional
from pydantic import BaseModel, Field, model_validator, ConfigDict
from datetime import datetime


class DataSchema(BaseModel):
    _id: Optional[str]
    symbol: str
    closing_price: float
    volume: int
    period_year: int
    period_month: int
    period_date: datetime
    unix_month_time: int

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "_id": "6678c9f7faac3e312c854822",
                "symbol": "TSLA",
                "closing_price": 191.080,
                "volume": 1017445313,
                "period_year": 2024,
                "period_month": 5,
                "period_date": "2023-01-31T00:00:00.000+00:00",
            }
        }
    )


class MetaDataSchema(BaseModel):
    _id: Optional[str]
    symbol: str
    information: str
    last_refresh: datetime
    time_zone: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "TSLA",
                "information": "Monthly Adjusted Prices and Volumes",
                "last_refresh": "2024-05-30",
                "time_zone": "US/Eastern",
            }
        }
    )


class ExternalMetaDataSchema(BaseModel):
    information: Optional[str] = Field(alias="1. Information")
    symbol: Optional[str] = Field(alias="2. Symbol")
    last_refresh: Optional[datetime] = Field(alias="3. Last Refreshed")
    time_zone: Optional[str] = Field(..., alias="4. Time Zone")

    @model_validator(mode="after")
    @classmethod
    def validate_date_keys(cls, values):
        if "3. Last Refreshed" in values:
            try:
                values["3. Last Refreshed"] = datetime.strptime(
                    values["3. Last Refreshed"], "%Y-%m-%d"
                )
            except (TypeError, ValueError):
                values["3. Last Refreshed"] = datetime.now()
        return values


class ExternalDataSchema(BaseModel):
    closing_price: Optional[float] = Field(alias="4. close")
    volume: Optional[int] = Field(alias="6. volume")
    dividend_amount: Optional[float] = Field(..., alias="7. dividend amount")

    @model_validator(mode="before")
    @classmethod
    def convert_close_and_volume(cls, values):
        if "4. close" in values:
            try:
                values["4. close"] = float(values["4. close"])
            except (TypeError, ValueError):
                values["4. close"] = 0
        else:
            values["4. close"] = 0
        if "6. volume" in values:
            try:
                values["6. volume"] = int(values["6. volume"])
            except (TypeError, ValueError):
                values["6. volume"] = 0
        else:
            values["6. volume"] = 0
        if "7. dividend amount" in values:
            try:
                values["7. dividend amount"] = float(values["7. dividend amount"])
            except (TypeError, ValueError):
                values["7. dividend amount"] = 0
        else:
            values["7. dividend amount"] = 0
        return values


class ExternalResponseDataSchema(BaseModel):
    meta_data: ExternalMetaDataSchema = Field(..., alias="Meta Data")
    monthly_adjusted_time_series: Dict[str, ExternalDataSchema] = Field(
        ..., alias="Monthly Adjusted Time Series"
    )


class SymbolLookUpResponse(BaseModel):
    symbol: Optional[str] = Field(alias="1. symbol")
    name: Optional[str] = Field(alias="2. name")
    type: Optional[str] = Field(alias="3. type")
    match_score: Optional[str] = Field(alias="9. matchScore")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "symbol": "TSLA",
                "name": "Tesla Inc.",
                "type": "Equity",
                "match_score": "0.7273",
            }
        }
    )


class EfficientResponseSummary(BaseModel):
    max: float
    min: float


class EfficientDataResponse(BaseModel):
    source: str
    columns: list[str]
    data: list[list[int | float]]
    summary: EfficientResponseSummary

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "columns": ["unix_month_time", "TSLA"],
                "data": [
                    [1717200000, 1714521600, 1711929600],
                    [172.46, 166.85, 166.2],
                ],
                "summary": {"max": 1980, "min": 27.0},
            }
        }
    )
