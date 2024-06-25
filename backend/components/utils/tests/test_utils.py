import unittest, os, sys
from datetime import datetime
import pandas as pd

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(path))
from utils.utils import Utils

from schemas.schemas import (
    ExternalResponseDataSchema,
    DataSchema,
)


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.external_data = {
            "Meta Data": {
                "1. Information": "Monthly Adjusted Prices and Volumes",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2024-06-24",
                "4. Time Zone": "US/Eastern",
            },
            "Monthly Adjusted Time Series": {
                "2024-06-24": {
                    "1. open": "166.5400",
                    "2. high": "178.4599",
                    "3. low": "163.5300",
                    "4. close": "175.020",
                    "5. adjusted close": "175.0200",
                    "6. volume": "56688578",
                    "7. dividend amount": "0.0000",
                },
            },
        }

    def test_standardize_external_data(self):
        standardized_data = Utils.standardize_external_data(
            ExternalResponseDataSchema(**self.external_data)
        )
        expected_data = [
            DataSchema(
                symbol="IBM",
                closing_price=175.020,
                volume=56688578,
                period_year=2024,
                period_month=6,
                period_date=datetime(2024, 6, 24, 0, 0),
                unix_month_time=1717200000,
            ),
        ]
        self.assertEqual(len(standardized_data), len(expected_data))

    def test_return_efficient_response(self):
        standardized_data = Utils.standardize_external_data(
            ExternalResponseDataSchema(**self.external_data)
        )
        efficient_response = Utils.return_efficient_response(standardized_data)
        expected_columns = ["unix_month_time", "IBM"]
        expected_data = [[1717200000], [175.02]]
        expected_summary = {"max": 175.02, "min": 175.02}
        self.assertEqual(efficient_response["columns"], expected_columns)
        self.assertEqual(efficient_response["data"], expected_data)
        self.assertEqual(efficient_response["summary"], expected_summary)


if __name__ == "__main__":
    unittest.main()
