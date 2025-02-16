<div align="center">

# **Stocknear: Open Source Stock Analysis Platform**

<h3>

[Homepage](https://stocknear.com/) | [Discord](https://discord.com/invite/hCwZMMZ2MT)

</h3>

[![GitHub Repo stars](https://img.shields.io/github/stars/stocknear/backend)](https://github.com/stocknear/backend/stargazers)

</div>

# Techstack

This is the codebase that powers [stocknear's](https://stocknear.com/) backend, which is an open-source stock analysis research platform.

Built with:

- [FastAPI](https://fastapi.tiangolo.com/): Python Backend
- [Fastify](https://fastify.dev/): Nodejs Backend
- [Pocketbase](https://pocketbase.io/): Database
- [Redis](https://redis.io/): Caching Data

# Contributing

Stocknear is an open-source project, soley maintained by Muslem Rahimi.

We are not accepting pull requests. However, you are more than welcome to fork the project and customize it to suit your needs.

The core idea of stocknear shall always be: **_Fast_**, **_Simple_** & **_Efficient_**.

# Support ❤️

If you love the idea of stocknear and want to support our mission you can help us in two ways:

- Become a [Pro Member](https://stocknear.com/pricing) of stocknear to get unlimited feature access to enjoy the platform to the fullest.
- You can sponsor us via [Github](https://github.com/sponsors/stocknear) to help us pay the servers & data providers to keep everything running!

# Building

## DB Setup

First, you need to create the databases, tables and json files. You can do this by running the following commands (inside app/):

Add MOCK_API=true to the first 4 commands to use the mock data instead of the real API data.

```
MOCK_API=true python3 create_crypto_db.py
MOCK_API=true python3 create_etf_db.py
MOCK_API=true python3 create_stock_db.py
MOCK_API=true python3 create_institute_db.py

python3 ta_signal.py
cp backup_db/* .

mkdir -p json/quote
mkdir -p json/pre-post-quote
MOCK_API=true python3 cron_quote.py

mkdir -p json/one-day-price
MOCK_API=true python3 cron_one_day_price.py

mkdir -p json/stockdeck
python3 cron_stockdeck.py

mkdir -p json/stock-screener
python3 restart_json.py
```

For the hedge funds data to populate, you need to run `python3 cron_hedge_funds.py`

For the historical stock price to populate, you need:
```
mkdir -p json/historical-price/one-week
mkdir -p json/historical-price/one-month
mkdir -p json/historical-price/six-months
mkdir -p json/historical-price/one-year
mkdir -p json/historical-price/five-years
mkdir -p json/historical-price/max

MOCK_API=true python3 cron_historical_price.py
```

For the stock's financials:
```
MOCK_API=true python3 cron_financial_statements.py
```

Requirements: docker

You can build a container with the code in this repo by running
`make build-docker`

It will take the local version of the code (with your changes in, if any) and use it.
To start the container, run `make compose`

In case you built the container and wants to access its shell for debugging, you can do so with `make docker-bash`

# Running locally

Before you do that, you want the following env variables to be set (the .env file should be inside of docker-compose):
```
UVICORN_BASE_URL=backend
USER_API_KEY=test
API_PORT=8000
BACKEND_NETWORK=backend-network
```

Requirements: docker-compose

Using docker-compose, you can bring up the containers needed to run the backend (backend app + redis for caching).

```
stocknear-backend/ (main) $ make compose                                                                                                                                                [5:48:44]
Creating network "docker-compose_backend" with the default driver
Creating network "docker-compose_redis" with the default driver
Creating docker-compose_redis_1   ... done
Creating docker-compose_backend_1 ... done
Attaching to docker-compose_redis_1, docker-compose_backend_1
redis_1    | 1:C 27 Jan 2025 05:47:23.126 # WARNING Memory overcommit must be enabled! Without it, a background save or replication may fail under low memory condition. Being disabled, it can also cause failures without low memory condition, see https://github.com/jemalloc/jemalloc/issues/1328. To fix this issue add 'vm.overcommit_memory = 1' to /etc/sysctl.conf and then reboot or run the command 'sysctl vm.overcommit_memory=1' for this to take effect.
redis_1    | 1:C 27 Jan 2025 05:47:23.126 * oO0OoO0OoO0Oo Redis is starting oO0OoO0OoO0Oo
redis_1    | 1:C 27 Jan 2025 05:47:23.126 * Redis version=7.4.2, bits=64, commit=00000000, modified=0, pid=1, just started
redis_1    | 1:C 27 Jan 2025 05:47:23.126 # Warning: no config file specified, using the default config. In order to specify a config file use redis-server /path/to/redis.conf
redis_1    | 1:M 27 Jan 2025 05:47:23.127 * monotonic clock: POSIX clock_gettime
redis_1    | 1:M 27 Jan 2025 05:47:23.127 * Running mode=standalone, port=6379.
redis_1    | 1:M 27 Jan 2025 05:47:23.128 * Server initialized
redis_1    | 1:M 27 Jan 2025 05:47:23.128 * Ready to accept connections tcp
backend_1  | Traceback (most recent call last):
backend_1  |   File "/opt/stocknear-backend/app/main.py", line 116, in <module>
backend_1  |     cursor.execute("SELECT DISTINCT symbol FROM stocks")
backend_1  | sqlite3.OperationalError: no such table: stocks
docker-compose_backend_1 exited with code 1
^CGracefully stopping... (press Ctrl+C again to force)
Stopping docker-compose_redis_1   ... done
```

TODO: Note that if the required databases (sqlite3) are not present, the backend container will fail. We dont have the db and table creation automated just yet, so to make it work you would need to create that yourself. There are some scripts that do it among all the crons inside `./app/`, which can be helpful.

Stop the containers:

```
make compose-down                                                                                                                                           [5:48:56]
Removing docker-compose_redis_1   ... done
Removing docker-compose_backend_1 ... done
Removing network docker-compose_backend
Removing network docker-compose_redis
```

# Issues

- Code currently relies on a bunch of environment variables, which need to be mapped somewhere (and provide descriptive errors if they are missing)
- It is assumed in the code that the DB is local. That doesnt scale for any serious application, so probably could use some refactoring it to allow remote data storage
