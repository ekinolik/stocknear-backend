from db import DBClass

class StockDatabase(DBClass):
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


    def _create_ticker_table(self, symbol):
        cleaned_symbol = symbol
        self.cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS '{cleaned_symbol}' (
                date TEXT UNIQUE,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume INT,
                change_percent FLOAT
            );
        """)
        self.conn.commit()
