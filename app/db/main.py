#! /usr/bin/env python3

import os
import time
import sys
import logging
import sqlite3

from dotenv import load_dotenv

import etf,stocks,crypto,institute

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger("init-db")

load_dotenv()

# directory where the local db files will be created.
# TODO: external db?
default_db_path = "/opt/stocknear/db"
DB_PATH = os.getenv("DB_PATH", default_db_path)

# all db classes we need here
ALL_DBS = [etf.ETFDatabase, 
          stocks.StockDatabase, 
          crypto.CryptoDatabase, 
          institute.InstituteDatabase]

if __name__ == "__main__":

    start = time.time()

    existing_db_files = os.listdir(DB_PATH)

    failed = []

    for db_class in ALL_DBS:
        if db_class._db_file() not in existing_db_files:
            log.info(f"{db_class._db_file()} not found in the db path at {DB_PATH}. will create it")
        elif os.path.isfile(f"{DB_PATH}/{db_class._db_file()}"):
            log.info(f"db {db_class._db_file()} already exists. creating the tables if missing")
        else:
            # path exists but it is not a file?? something is not right, but lets ignore and continue anyway
            log.error(f"path {db_class._db_file()} already exists at {DB_PATH}, but it is not a file?! ignoring anyway")
            continue

        try:
            conn = sqlite3.connect(f"{DB_PATH}/{db_class._db_file()}")
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode = wal")
            conn.commit()

            db = db_class(conn)
            db._create_table()

            print(db.table_info())
            
        except Exception as e:
            raise RuntimeError(f"encountered an error while trying to create {db_class._db_file()}: {e}")

    log.info(f"finished creating databases. duration: {(time.time() - start):.2f}")
    sys.exit(0)