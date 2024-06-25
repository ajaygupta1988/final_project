from schemas import ExternalResponseDataSchema, DataSchema, EfficientDataResponse
from datetime import datetime
from calendar import timegm
import pandas as pd


class Utils:
    def __init__(self) -> None:
        pass

    @staticmethod
    def standardize_external_data(data: ExternalResponseDataSchema) -> list[DataSchema]:
        result = []
        for key, value in data.monthly_adjusted_time_series.items():
            period_date = datetime.strptime(key, "%Y-%m-%d")
            unix_time = timegm(
                datetime(period_date.year, period_date.month, 1, 0, 0, 0).timetuple()
            )
            value_to_insert = {
                "symbol": data.meta_data.symbol,
                "closing_price": value.closing_price,
                "volume": value.volume,
                "period_year": period_date.year,
                "period_month": period_date.month,
                "period_date": period_date,
                "unix_month_time": unix_time,
            }
            result.append(value_to_insert)
        return result

    @staticmethod
    def return_efficient_response(data: DataSchema) -> EfficientDataResponse:
        result = {"columns": [], "data": [], "summary": {}}

        df = pd.DataFrame(data)[["unix_month_time", "symbol", "closing_price"]]
        ticker_value = df["symbol"].unique()[0]
        df = df.drop("symbol", axis=1).rename(columns={"closing_price": ticker_value})
        max = df[ticker_value].max()
        min = df[ticker_value].min()
        result["columns"] = df.columns.to_list()
        result["data"] = []
        for col in result["columns"]:
            result["data"].append(df[col].to_list())
        result["summary"]["max"] = max
        result["summary"]["min"] = min
        return result
