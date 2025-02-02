import json
from db import DBClass

class StockDatabase(DBClass):

    # stocks table
    STOCKS_FIELDS = [
        "symbol" # pk
        "name",
        "exchange",
        "exchangeShortName",
        "type",
    ]

    # per ticker tables, historical price information.
    STOCK_TICKER_FIELDS = [
        "date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "change_percent",
    ]

    db_file = "stocks.db"

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    @classmethod
    def _db_file(cls):
        return "stocks.db"

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS stocks (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            exchange TEXT,
            exchangeShortName TEXT,
            type TEXT
        )
        """)
        self.conn.commit()

    def delete(self, symbol: str):
        self.cursor.execute("BEGIN TRANSACTION")

        self.cursor.execute("DELETE FROM stocks WHERE symbol = ?", (symbol,))
        self.cursor.execute(f"DROP TABLE {symbol}")

        self.cursor.execute("COMMIT")
        self.conn.commit()


    def add(self, **kwargs):
        symbol = kwargs.get("symbol")

        # make sure we have all the fields
        for col in STOCKS_FIELDS:
            if col not in kwargs:
                raise ValueError(f"can't insert into stocks table, field {col} missing for {symbol}")

        for col in STOCK_TICKER_FIELDS:
            if col not in kwargs:
                raise ValueError(f"can't create stock ticker table, field {col} missing for {symbol}")


        # get arguments for each of the updates
        cols, vals = {col: val for col, val in kwargs.items() if col in STOCKS_FIELDS}
        symbol_cols, symbol_vals = {col: val for col, val in kwargs.items() if col in STOCK_TICKER_FIELDS}

        self.cursor.execute("BEGIN TRANSACTION")

        self.cursor.execute(f"""
            INSERT OR IGNORE INTO stocks (, {cols.join(",")})
            VALUES (?)
            """, (vals.join(","))
            )
    
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS '{symbol}' (
                date TEXT UNIQUE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume INT,
                change_percent FLOAT
            );
        """)

        self.cursor.execute(f"""
            INSERT OR IGNORE INTO {symbol} (, {cols.join(",")})
            VALUES (?)
            """, (vals.join(","))
            )

        self.cursor.execute("COMMIT")

        self.conn.commit()

    def table_info(self):
        self.cursor.execute("PRAGMA table_info(stocks)")
        result = {"stocks": {x[1]: x[2] for x in self.cursor.fetchall()}}
        return json.dumps(result)