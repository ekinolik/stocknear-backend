#! /usr/bin/env python3

import os
import time
import sys
import logging

import etf,stocks,crypto,institute

log = logging.getLogger(__name__)

load_dotenv()

# directory where the local db files will be created.
# TODO: external db?
default_db_path = "/opt/stocknear/db"
DB_PATH = os.getenv("DB_PATH", default_db_path)

# external api keys. make it a dict so its easier to pass to our database classes
API_KEYS = {
    "FMP_API_KEY": os.getenv("FMP_API_KEY", None),
    "BENZINGA_API_KEY": os.getenv("BENZINGA_API_KEY", None),
    "COINGECKO_API_KEY":  os.getenv("COINGECKO_API_KEY", None),
}

# all db classes we need here
ALL_DBS = [etf.ETFDatabase, 
          stocks.StockDatabase, 
          crypto.CryptoDatabase, 
          institute.InstituteDatabase]

if __name__ == "__main__":

    start = time.time()

    # we need these api keys to load the databases
    for keyname, keyval in API_KEYS.items():
        if keyval is None:
            raise ValueError(f"{keyname} not defined")

    existing_db_files = os.listdir(DB_PATH)

    # we only update DBs that dont exist yet.
    # check our path to see which table is missing and create it.
    # if a db file already exists, it is left untouched.
    missing_dbs = []

    for db_class in ALL_DBS:
        if db_class.db_file not in existing_db_files:
            log.info(f"{db_class.db_file} not found in the db path at {DB_PATH}. will create it")
            missing_dbs.append(db_class)
        elif os.path.isfile(f"{DB_PATH}/{db_class.db_file}"):
            log.info(f"db {db_class.db_file} already exists")
        else:
            # path exists but it is not a file?? something is not right, but lets ignore and continue anyway
            log.error(f"path {db_class.db_file} already exists at {DB_PATH}, but it is not a file?! ignoring anyway")

    if not missing_dbs:
        log.info("no dbs are missing. nothing to do")
        os.exit(0)

    failed = []

    for db_class in missing_dbs:
        try:
            db = db_class(DB_PATH)
            db.create_db()
            db.populate(API_KEYS)
        except Exception as e:
            log.error(f"encountered an error while trying to create f{db_class.db_file}: {e}")
            failed.append(db_class)

    if failed:
        log.error(f"failed to load one or more databases: {[x.db_path for x in failed]}")
        sys.exit(1)

    log.info(f"finished loading {len(missing_dbs)} databases. duration: {time.time() - start:.2f:}")
    sys.exit(0)