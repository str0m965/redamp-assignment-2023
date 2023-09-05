import os

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from .schema import BaseEntity, DataSource


def get_engine():
    pg_password = os.environ.get('PG_PASSWORD')
    pg_user = os.environ.get('PG_USER', 'postgres')
    pg_port = os.environ.get('PG_PORT', 5432)
    pg_host = os.environ.get('PG_HOST', 'localhost')
    pg_db = os.environ.get('PG_DB', 'ioc_sync')
    return create_engine(f'postgresql+psycopg2://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}', echo=False)


def get_session(engine):
    return Session(engine)


def recreate_all(seed=True):
    engine = get_engine()
    BaseEntity.metadata.drop_all(engine)
    BaseEntity.metadata.create_all(engine)
    if seed:
        with Session(engine) as session:
            new_data_sources = \
                [
                    DataSource(url="https://urlhaus.abuse.ch/downloads/csv_recent/", alias="urlhaus"),
                    DataSource(url="http://reputation.alienvault.com/reputation.data", alias="alienvault"),
                    DataSource(url="https://openphish.com/feed.txt", alias="openphish")
                ]
            session.add_all(new_data_sources)
            session.commit()
