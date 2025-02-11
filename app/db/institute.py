import json
from db import DBClass

class InstituteDatabase(DBClass):

    ## Consists of a single INSTITUTE table.
    ## the table contains the fields of the FMP summary info (can find that in the mock_responses),
    ## a field storing the holdings as a json blob, and some extra fields like winRate and numberOfStocks

    INSTITUTE_FIELDS = [
        "date",
        "name",
        "cik", ## Primary Key
        "portfolioSize",
        "performance3yearRelativeToSP500Percentage",
        "performance5yearRelativeToSP500Percentage",
        "performanceSinceInceptionRelativeToSP500Percentage",
        "winRate",
        "holdings",
    ]

    HOLDINGS_FIELDS = [
        "symbol",
        "securityName",
        "weight",
        "sharesNumber",
        "changeInSharesNumberPercentage",
        "putCallShare",
        "marketValue",
        "avgPricePaid",
    ]

    def __init__(self, conn):
        self.conn = conn
        self.cursor = self.conn.cursor()

    @classmethod
    def _db_file(cls):
        return "institute.db"

    def _create_table(self):
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS institutes (
            cik TEXT PRIMARY KEY,
            name TEXT,
            date TEXT,
            portfolioSize REAL,
            performance3yearRelativeToSP500Percentage REAL,
            performance5yearRelativeToSP500Percentage REAL,
            performanceSinceInceptionRelativeToSP500Percentage REAL,
            winRate REAL,
            numberOfStocks INTEGER,
            holdings TEXT
        )
        """)
        self.conn.commit()

    def delete(self, cik: str):
        self.cursor.execute("DELETE FROM institutes WHERE cik = ?", (cik,))
        self.conn.commit()

    def add(self, **kwargs):
        # filter out unknown fields.
        # here we expect to have a dictionary matching our known fields defined in the class
        column_values = {col:val for col,val in kwargs.items() if col in self.INSTITUTE_FIELDS}
        cik = column_values.pop("cik", None)
        name = column_values.pop("name", "uknown")
        if not cik:
            raise ValueError("cik not present in the dictionary. cant match an institution without it")

        self.cursor.execute("BEGIN TRANSACTION")

        self.cursor.execute(f"""
            INSERT OR IGNORE INTO institutes (cik, name)
            VALUES (?, ?)
            """, (cik, name)
            )
        for col, val in column_values.items():
            self.cursor.execute(f"""
                UPDATE institutes 
                SET {col} = {val}
                WHERE cik = {cik}""")

        self.cursor.execute("COMMIT")
                
        self.conn.commit()

    def table_info(self):
        self.cursor.execute("PRAGMA table_info(institutes)")
        result = {"institutes": {x[1]: x[2] for x in self.cursor.fetchall()}}
        return json.dumps(result)