import unittest, os, sys
from unittest.mock import patch, MagicMock
from mongomock_motor import AsyncMongoMockClient

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(path))

from components import QueryManager
from schemas import (
    ExternalResponseDataSchema,
)
from config import settings


class TestQueryManager(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        # Initialize a mongomock client
        self.mongo_client = AsyncMongoMockClient()
        self.loader = QueryManager(client=self.mongo_client)

        self.database = self.mongo_client[settings.database]
        self.data_collection = self.database.get_collection("data_collection")
        self.meta_data_collection = self.database.get_collection("meta_data_collection")

        self.fresh_data = {
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
                    "4. close": "175.0200",
                    "5. adjusted close": "175.0200",
                    "6. volume": "56688681",
                    "7. dividend amount": "0.0000",
                },
            },
        }

        self.stale_data = {
            "Meta Data": {
                "1. Information": "Monthly Adjusted Prices and Volumes",
                "2. Symbol": "IBM",
                "3. Last Refreshed": "2024-06-12",
                "4. Time Zone": "US/Eastern",
            },
            "Monthly Adjusted Time Series": {
                "2024-06-24": {
                    "1. open": "166.5400",
                    "2. high": "178.4599",
                    "3. low": "163.5300",
                    "4. close": "175.0200",
                    "5. adjusted close": "175.0200",
                    "6. volume": "56688681",
                    "7. dividend amount": "0.0000",
                },
            },
        }

    async def asyncTearDown(self):
        await self.mongo_client.drop_database(settings.database)

    async def test_add_data_from_api(self):
        # Prepare test data
        data = ExternalResponseDataSchema(**self.fresh_data)

        # Call add_data_from_api method
        add_response = await self.loader.add_data_from_api(data)

        inserted_data = await self.loader.get_symbol_data("IBM")

        self.assertIsNotNone(inserted_data)

        self.assertEqual(add_response, {"detail": "data successfully inserted"})

    async def test_missing_data(self):
        # When meta data record is not found, check_if_data_is_missing_or_stale should return True
        result = await self.loader.check_if_data_is_missing_or_stale("AAPL")
        self.assertTrue(result)

    async def test_stale_data(self):
        # When last_refreshed date is older than 10 days, check_if_data_is_missing_or_stale should return True

        # adding stale data
        data = ExternalResponseDataSchema(**self.stale_data)

        # Call add_data_from_api method
        add_response = await self.loader.add_data_from_api(data)

        result = await self.loader.check_if_data_is_missing_or_stale(
            "IBM", stale_duration_days=10
        )
        self.assertTrue(result)

    async def test_fresh_data(self):
        # When last_refreshed date is within 10 days, check_if_data_is_missing_or_stale should return False

        # When last_refreshed date is older than 10 days, check_if_data_is_missing_or_stale should return True

        # adding fresh data
        data = ExternalResponseDataSchema(**self.fresh_data)

        # Call add_data_from_api method
        add_response = await self.loader.add_data_from_api(data)

        result = await self.loader.check_if_data_is_missing_or_stale(
            "IBM", stale_duration_days=10
        )
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
