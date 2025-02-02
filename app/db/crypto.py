from db import DBClass

class CryptoDatabase(DBClass):

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    @classmethod
    def _db_file(cls):
        return "crypto.db"

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS cryptos (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            exchange TEXT,
            type TEXT
        )
        """)
        self.conn.commit()
