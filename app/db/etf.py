import json
from db import DBClass

class ETFDatabase(DBClass):

    ETF_FIELDS = [
        "symbol", # primary key
        "name",
        "exchange",
        "exchangeShortName",
        "type",
    ]

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    @classmethod
    def _db_file(cls):
        return "etf.db"

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS etfs (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            exchange TEXT,
            exchangeShortName TEXT,
            type TEXT
        )
        """)
        self.conn.commit()

    def delete(self, symbol: str):
        self.cursor.execute("DELETE FROM etfs WHERE symbol = ?", (symbol,))
        self.conn.commit()

    def add(self, **kwargs):
        column_values = {col:val for col, val in kwargs.items() if col in self.ETF_FIELDS}
        symbol = column_values.pop("symbol", None)
        if not symbol:
            raise ValueError("symbol not passed in the dict, cant match an etf entry without it.")

        self.cursor.execute("BEGIN TRANSACTION")

        self.cursor.execute(f"""
            INSERT OR IGNORE INTO etfs (symbol)
            VALUES (?)
            """, (symbol,)
            )
        for col, val in column_values.items():
            self.cursor.execute(f"""
                UPDATE etfs 
                SET {col} = {val}
                WHERE symbol = {symbol}""")

        self.cursor.execute("COMMIT")
                
        self.conn.commit()

    def table_info(self):
        self.cursor.execute("PRAGMA table_info(etfs)")
        result = {"etfs": {x[1]: x[2] for x in self.cursor.fetchall()}}
        return json.dumps(result)