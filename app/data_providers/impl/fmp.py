from typing import Callable
from data_providers.impl.constants import FMP_BASE_URL


class FinancialModelingPrep:
    def __init__(self, fetcher: Callable[[str], dict], api_key: str):
        self.api_key = api_key
        self.fetcher = fetcher

    async def list_traded_stocks(self) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/available-traded/list?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def list_institutional_ownership(self) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/institutional-ownership/list?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_portfolio_holdings_summary(self, cik: str, page: int = 0) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/institutional-ownership/portfolio-holdings-summary?cik={cik}&page={page}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_portfolio_holdings(self, cik: str, quarter_date: str, page: int = 0) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/institutional-ownership/portfolio-holdings?cik={cik}&date={quarter_date}&page={page}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def list_available_traded(self) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/available-traded/list?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_company_profile(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/profile/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_stock_dividend(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/historical-price-full/stock_dividend/{symbol}?limit=400&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_employee_count(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/historical/employee_count?symbol={symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_stock_split(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/historical-price-full/stock_split/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_stock_peers(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/stock_peers?symbol={symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_institutional_holders(self, symbol: str, date: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/institutional-ownership/institutional-holders/symbol-ownership-percent?date={date}&symbol={symbol}&page=0&apikey={self.api_key}"
        return (await self.fetcher(url))
    
    async def get_shares_float(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/historical/shares_float?symbol={symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_revenue_product_segmentation(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/revenue-product-segmentation?symbol={symbol}&structure=flat&period=annual&apikey={self.api_key}"
        return (await self.fetcher(url))
    

    async def get_revenue_geographic_segmentation(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/revenue-geographic-segmentation?symbol={symbol}&structure=flat&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_analyst_estimates(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/analyst-estimates/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_quote(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/quote/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_historical_price_full(self, symbol: str, from_date: str, to_date: str, serie_type: str = 'bar') -> dict:
        url = f"{FMP_BASE_URL}/api/v3/historical-price-full/{symbol}?serietype={serie_type}&from={from_date}&to={to_date}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_etf_info(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/etf-info?symbol={symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_etf_holder(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/etf-holder/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_etf_country_weightings(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/etf-country-weightings/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def list_etfs(self) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/etf/list?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def list_available_cryptocurrencies(self) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/symbol/available-cryptocurrencies?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_batch_pre_post_market_trade(self, symbols: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/batch-pre-post-market-trade/{symbols}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_batch_pre_post_market(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/batch-pre-post-market/{symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_historical_chart(self, symbol: str, from_date: str, to_date: str, interval: str = '1min') -> dict:
        url = f"{FMP_BASE_URL}/api/v3/historical-chart/{interval}/{symbol}?from={from_date}&to={to_date}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_key_metrics(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/key-metrics/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_income_statement(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/income-statement/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_balance_sheet_statement(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/balance-sheet-statement/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_cash_flow_statement(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/cash-flow-statement/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_ratios(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/ratios/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_income_statement_growth(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/income-statement-growth/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_balance_sheet_statement_growth(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/balance-sheet-statement-growth/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_cash_flow_statement_growth(self, symbol: str, period: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/cash-flow-statement-growth/{symbol}?period={period}&apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_key_metrics_ttm(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v3/key-metrics-ttm/{symbol}?apikey={self.api_key}"
        return (await self.fetcher(url))

    async def get_owner_earnings(self, symbol: str) -> dict:
        url = f"{FMP_BASE_URL}/api/v4/owner_earnings?symbol={symbol}&apikey={self.api_key}"
        return (await self.fetcher(url))