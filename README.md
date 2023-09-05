# ioc sync

## Usage

```bash
# set environment variables
PG_PASSWORD=<password>
PG_USER=<user>
PG_PORT=<port>
PG_HOST=<host>
PG_DB=<db>

# initialize database(also adds default data sources)
python -m ioc_sync init-db

# update ioc from data sources
python -m ioc_sync update-all

# find ioc in database
python -m ioc_sync find-one-ip <ip>
python -m ioc_sync find-one-url <url>
```