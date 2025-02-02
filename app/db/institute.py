from db import DBClass

class InstituteDatabase(DBClass):

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
            name TEXT
        )
        """)
        self.conn.commit()

    def delete(stlf, cik: str):
        self.cursor.execute("DELETE FROM institutes WHERE cik = ?", (cik,))
        self.conn.commit()

    def add(stlf, cik, name: str):
        self.cursor.execute("""
            INSERT OR IGNORE INTO institutes (cik, name)
            VALUES (?, ?)
            """, (cik, name)
            )
        self.cursor.execute("""
            UPDATE institutes SET name = ?
            WHERE cik = ?
            """, (name, cik)
            )
        self.conn.commit()