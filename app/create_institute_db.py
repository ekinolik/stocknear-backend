import aiohttp
import asyncio
import sqlite3
import certifi
import json
import pandas as pd
from tqdm import tqdm
import re
import pandas as pd
from datetime import datetime
import subprocess
import time
import warnings
from dotenv import load_dotenv
import os
import re
from data_providers.fetcher import get_fetcher
from data_providers.impl.fmp import FinancialModelingPrep

# Filter out the specific RuntimeWarning
warnings.filterwarnings("ignore", category=RuntimeWarning, message="invalid value encountered in scalar divide")

def normalize_name(name):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', name.lower())).strip()


con = sqlite3.connect('backup_db/stocks.db')
etf_con = sqlite3.connect('backup_db/etf.db')
crypto_con = sqlite3.connect('backup_db/crypto.db')

cursor = con.cursor()
cursor.execute("PRAGMA journal_mode = wal")
cursor.execute("SELECT DISTINCT symbol, name FROM stocks WHERE symbol NOT LIKE '%.%'")
stock_data = [{
    'symbol': row[0],
    'name': row[1],
} for row in cursor.fetchall()]
# Create a dictionary from stock_data for quick lookup
stock_dict = {normalize_name(stock['name']): stock['symbol'] for stock in stock_data}
stock_symbols = [item['symbol'] for item in stock_data]

etf_cursor = etf_con.cursor()
etf_cursor.execute("PRAGMA journal_mode = wal")
etf_cursor.execute("SELECT DISTINCT symbol, name FROM etfs")
etf_data = [{
    'symbol': row[0],
    'name': row[1],
} for row in etf_cursor.fetchall()]
# Create a dictionary from stock_data for quick lookup
etf_dict = {normalize_name(etf['name']): etf['symbol'] for etf in etf_data}
etf_symbols = [item['symbol'] for item in etf_data]


crypto_cursor = crypto_con.cursor()
crypto_cursor.execute("PRAGMA journal_mode = wal")
crypto_cursor.execute("SELECT DISTINCT symbol FROM cryptos")
crypto_symbols = [row[0] for row in crypto_cursor.fetchall()]

total_symbols = stock_symbols + etf_symbols + crypto_symbols
con.close()
etf_con.close()
crypto_con.close()


load_dotenv()
api_key = os.getenv('FMP_API_KEY')
quarter_date = '2024-09-30'
fmp = FinancialModelingPrep(get_fetcher(json_mode=True), api_key)



if os.path.exists("backup_db/institute.db"):
    os.remove('backup_db/institute.db')


def get_jsonparsed_data(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError:
        return {}


class InstituteDatabase:
    def __init__(self, db_path):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("PRAGMA journal_mode = wal")
        self.conn.commit()
        self._create_table()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS institutes (
            cik TEXT PRIMARY KEY,
            name TEXT
        )
        """)


    def get_column_type(self, value):
        column_type = ""

        if isinstance(value, str):
            column_type = "TEXT"
        elif isinstance(value, int):
            column_type = "INTEGER"
        elif isinstance(value, float):
            column_type = "REAL"
        else:
            # Handle other data types or customize based on your specific needs
            column_type = "TEXT"

        return column_type

    def remove_null(self, value):
        if isinstance(value, str) and value == None:
            value = 'n/a'
        elif isinstance(value, int) and value == None:
            value = 0
        elif isinstance(value, float) and value == None:
            value = 0
        else:
            # Handle other data types or customize based on your specific needs
            pass

        return value




    async def save_portfolio_data(self, session, cik):
        try:
            # Fetch summary data
            summary_parsed_data = await fmp.get_portfolio_holdings_summary(cik)

            portfolio_data = {}
            holdings_data = []

            # Fetch paginated holdings data
            for page in range(0,100):
                parsed_data = await fmp.get_portfolio_holdings(cik, quarter_date, page)

                if not parsed_data:  # Stop if no more data
                    break

                if isinstance(parsed_data, list):
                    for item in parsed_data:
                        if item['symbol'] is None:
                            normalized_security_name = normalize_name(item['securityName'])
                            if normalized_security_name in stock_dict:
                                item['symbol'] = stock_dict[normalized_security_name]
                            elif normalized_security_name in etf_dict:
                                item['symbol'] = etf_dict[normalized_security_name]

                    parsed_data = [
                        {**item, 'type': ('stocks' if item['symbol'] in stock_symbols else
                                            'crypto' if item['symbol'] in crypto_symbols else
                                            'etf' if item['symbol'] in etf_symbols else None)}
                        for item in parsed_data
                        if 'symbol' in item and item['symbol'] is not None and item['symbol'] in total_symbols
                    ]

                    holdings_data.extend(parsed_data)
                    portfolio_data['holdings'] = json.dumps(holdings_data)

            if not holdings_data:
                self.cursor.execute("DELETE FROM institutes WHERE cik = ?", (cik,))
                self.conn.commit()
                return

            performance_percentages = [item.get("performancePercentage", 0) for item in holdings_data]

            #Filter information out that is not needed (yet)!
            holdings_data = [{"symbol": item["symbol"], "securityName": item["securityName"], 'weight': item['weight'], 'sharesNumber': item['sharesNumber'], 'changeInSharesNumberPercentage': item['changeInSharesNumberPercentage'], 'putCallShare': item['putCallShare'], "marketValue": item["marketValue"], 'avgPricePaid': item['avgPricePaid']} for item in holdings_data]

            number_of_stocks = len(holdings_data)
            positive_performance_count = sum(1 for percentage in performance_percentages if percentage > 0)
            win_rate = round(positive_performance_count / len(performance_percentages) * 100, 2) if performance_percentages else 0

            portfolio_data.update({
                'winRate': win_rate,
                'numberOfStocks': number_of_stocks
            })

            # Process and add summary data
            if isinstance(summary_parsed_data, list) and summary_parsed_data:
                portfolio_data['summary'] = json.dumps(summary_parsed_data)
                # TODO: does the api actually have these fields? they are not documented, and not available on free tier
                data_dict = {
                    'marketValue': summary_parsed_data[0].get('marketValue', 0),
                    'averageHoldingPeriod': summary_parsed_data[0].get('averageHoldingPeriod', 0),
                    'turnover': summary_parsed_data[0].get('turnover', 0),
                    'performancePercentage': summary_parsed_data[0].get('performancePercentage', 0),
                    'performancePercentage3year': summary_parsed_data[0].get('performancePercentage3year', 0),
                    'performancePercentage5year': summary_parsed_data[0].get('performancePercentage5year', 0),
                    'performanceSinceInceptionPercentage': summary_parsed_data[0].get('performanceSinceInceptionPercentage', 0)
                }
                portfolio_data.update(data_dict)

            self.cursor.execute("PRAGMA table_info(institutes)")
            columns = {column[1]: column[2] for column in self.cursor.fetchall()}

            column_definitions = {
                key: (self.get_column_type(portfolio_data.get(key, None)), self.remove_null(portfolio_data.get(key, None)))
                for key in portfolio_data
            }

            for column, (column_type, value) in column_definitions.items():
                if column not in columns and column_type:
                    self.cursor.execute(f"ALTER TABLE institutes ADD COLUMN {column} {column_type}")

                self.cursor.execute(f"UPDATE institutes SET {column} = ? WHERE cik = ?", (value, cik))

            self.conn.commit()

        except Exception as e:
            print(f"Failed to fetch portfolio data for cik {cik}: {str(e)}")


    async def save_insitute(self, institutes):

        institute_data = []

        for item in institutes:
            cik = item.get('cik', '')
            name = item.get('name', '')


            institute_data.append((cik, name))
        

        self.cursor.execute("BEGIN TRANSACTION")  # Begin a transaction

        for data in institute_data:
            cik, name = data
            self.cursor.execute("""
            INSERT OR IGNORE INTO institutes (cik, name)
            VALUES (?, ?)
            """, (cik, name))
            self.cursor.execute("""
            UPDATE institutes SET name = ?
            WHERE cik = ?
            """, (name, cik))

        self.cursor.execute("COMMIT")  # Commit the transaction
        self.conn.commit()

       

        # Save OHLC data for each ticker using aiohttp
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            i = 0
            for item in tqdm(institute_data):
                cik, name = item
                tasks.append(self.save_portfolio_data(session, cik))

                i += 1
                if i % 300 == 0:
                    await asyncio.gather(*tasks)
                    tasks = []
                    print('sleeping mode: ', i)
                    await asyncio.sleep(60)  # Pause for 60 seconds

            
            if tasks:
                await asyncio.gather(*tasks)



db = InstituteDatabase('backup_db/institute.db')
loop = asyncio.get_event_loop()
all_tickers = loop.run_until_complete(fmp.list_institutional_ownership())
#all_tickers = [{'cik': '0001364742', 'name': "GARDA CAPITAL PARTNERS LP"}]
loop.run_until_complete(db.save_insitute(all_tickers))
db.close_connection()
