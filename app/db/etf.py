from db import DBClass

class ETFDatabase(DBClass):

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

