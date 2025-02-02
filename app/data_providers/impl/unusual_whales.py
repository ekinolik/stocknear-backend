from typing import Callable
from data_providers.impl.constants import UNUSUAL_WHALES_BASE_URL

class UnusualWhales:
    def __init__(self, fetcher: Callable[[str, dict], dict], api_key: str):
        self.fetcher = fetcher
        self.headers = {
            "Accept": 'application/json, text/plain',
            "Authorization": f"Bearer {api_key}"
        }   

    def get_option_contracts(self, symbol: str) -> dict:
        url = f"{UNUSUAL_WHALES_BASE_URL}/api/stock/{symbol}/option-contracts"
        return self.fetcher(url, self.headers)
