#! /usr/bin/env python3

import os
import time
import sys
import logging
import sqlite3

from dotenv import load_dotenv

import etf,stocks,crypto,institute

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
log = logging.getLogger(__name__)

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

    # we only create DBs that dont exist yet.
    # check our path to see which table is missing and create it.
    # if a db file already exists, it is left untouched.
    missing_dbs = []

    for db_class in ALL_DBS:
        if db_class._db_file() not in existing_db_files:
            log.info(f"{db_class._db_file()} not found in the db path at {DB_PATH}. will create it")
            missing_dbs.append(db_class)
        elif os.path.isfile(f"{DB_PATH}/{db_class._db_file()}"):
            log.info(f"db {db_class._db_file()} already exists")
        else:
            # path exists but it is not a file?? something is not right, but lets ignore and continue anyway
            log.error(f"path {db_class._db_file()} already exists at {DB_PATH}, but it is not a file?! ignoring anyway")

    if not missing_dbs:
        log.info("no dbs are missing. nothing to do")
        sys.exit(0)

    failed = []

    for db_class in missing_dbs:
        try:
            conn = sqlite3.connect(f"{DB_PATH}/{db_class._db_file()}")
            cursor = conn.cursor()
            cursor.execute("PRAGMA journal_mode = wal")
            conn.commit()

            db = db_class(conn)
            db._create_table()
        except Exception as e:
            log.error(f"encountered an error while trying to create {db_class._db_file()}: {e}")
            failed.append(db_class)

    if failed:
        log.error(f"failed to load one or more databases: {[x._db_file() for x in failed]}")
        sys.exit(1)

    log.info(f"finished loading {len(missing_dbs)} databases. duration: {(time.time() - start):.2f}")
    sys.exit(0)