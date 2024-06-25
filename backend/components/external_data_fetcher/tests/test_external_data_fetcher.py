import unittest, os, sys
from unittest.mock import patch, AsyncMock

path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(path))
from external_data_fetcher import ExternalDataFetcher


class TestExternalDataFetcher(unittest.IsolatedAsyncioTestCase):
    async def test_get_data_for_symbol_success(self):
        # Arrange
        symbol = "AAPL"
        expected_data = {"some": "data"}  # Replace with expected data structure

        async def mock_json():
            return expected_data

        # Patch the response.json() method to return expected data
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.json = mock_json
            mock_get.return_value.__aenter__.return_value = mock_response

            # Act
            fetcher = ExternalDataFetcher()
            data = await fetcher.get_data_for_symbol(symbol)

        # Assert
        self.assertEqual(data, expected_data)

    async def test_search_for_symbol_success(self):
        # Arrange
        keywords = "tesco"
        expected_data = []  # Replace with expected data structure

        async def mock_json():
            return {"bestMatches": []}

        # Patch the response.json() method to return expected data
        with patch("aiohttp.ClientSession.get") as mock_get:
            mock_response = AsyncMock()
            mock_response.json = mock_json
            mock_get.return_value.__aenter__.return_value = mock_response

            # Act
            fetcher = ExternalDataFetcher()
            data = await fetcher.search_for_symbol(keywords)

        # Assert
        self.assertEqual(data, expected_data)


if __name__ == "__main__":
    unittest.main()
