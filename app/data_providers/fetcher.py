import os
import aiohttp
from data_providers.mocks.mock_fetcher import mock_fetch_data_json, mock_fetch_data_response

async def real_fetch_data(url, headers={}):
    """Function to fetch real API responses."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            return await response.json()


def get_fetcher(json_mode: bool):
    """Decides whether to call the real API or use mock responses based on environment setting."""
    mock_mode = os.getenv("MOCK_API", "false").lower() == "true"

    if mock_mode:
        return mock_fetch_data_json if json_mode else mock_fetch_data_response
    else:
        return real_fetch_data