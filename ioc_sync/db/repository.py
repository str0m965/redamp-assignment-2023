from sqlalchemy import func
from sqlalchemy.dialects.postgresql import insert

from .connection import get_engine
from .schema import DataSource, IpIoc, UrlIoc
from sqlalchemy.orm import Session, contains_eager


class CommonRepository:
    def __init__(self, engine):
        self.engine = engine

    def get_data_sources(self) -> list[DataSource]:
        """
        Get all data sources
        :return:
        """
        with Session(self.engine) as session:
            return session.query(DataSource).all()

    def find_one_ip_ioc(self, ip) -> IpIoc:
        """
        Find one ip ioc
        :return:
        """
        with Session(self.engine) as session:
            return session.query(IpIoc)\
                .join(IpIoc.data_source)\
                .options(contains_eager(IpIoc.data_source))\
                .filter(IpIoc.ip == ip)\
                .first()

    def find_one_url_ioc(self, url) -> UrlIoc:
        """
        Find one url ioc
        :return:
        """
        with Session(self.engine) as session:
            return session.query(UrlIoc).join(UrlIoc.data_source).options(contains_eager(UrlIoc.data_source)).filter(UrlIoc.url == url).first()

    def upsert_url_iocs(self, urls: list[UrlIoc]):
        """
        Upsert url iocs
        :param urls:
        :return:
        """
        # consider pg copy or chunk data if performance is an issue
        insert_statement = insert(UrlIoc.__table__) \
            .values([
            {"url": url.url, "data_source_id": url.data_source.id} for url in urls]) \
            .on_conflict_do_update(constraint='url_data_source_uc', set_={'updated_at': func.now()})
        with Session(self.engine) as session:
            session.execute(insert_statement)
            session.commit()

    def upsert_ip_iocs(self, ips: list[IpIoc]):
        """
        Upsert ip iocs
        :param ips:
        :return:
        """
        # consider pg copy or chunk data if performance is an issue
        insert_statement = insert(IpIoc.__table__) \
            .values([
                {"ip": ip.ip, "data_source_id": ip.data_source.id} for ip in ips]) \
            .on_conflict_do_update(constraint='ip_data_source_uc', set_={'updated_at': func.now()})
        with Session(self.engine) as session:
            session.execute(insert_statement)
            session.commit()

    @classmethod
    def get_instance(cls):
        """
        Singleton factory method to get repository
        :return:
        """
        if not hasattr(cls, "_instance"):
            CommonRepository._instance = CommonRepository(get_engine())
        return CommonRepository._instance
