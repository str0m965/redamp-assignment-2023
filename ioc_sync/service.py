from .db.repository import CommonRepository
from .db.schema import UrlIoc, IpIoc
from .dtos import IocProcessor, IocType
from .http_gateway import HttpGateway


class CommonService:
    def __init__(self, repository: CommonRepository, http_gateway: HttpGateway):
        self.repository = repository
        self.http_gateway = http_gateway

    def get_data_sources(self):
        return self.repository.get_data_sources()

    def get_url_ioc(self, url):
        return self.repository.find_one_url_ioc(url)

    def get_ip_ioc(self, ip):
        return self.repository.find_one_ip_ioc(ip)

    def sync_all_iocs(self):
        data_sources = self.repository.get_data_sources()
        url_iocs = []
        ip_iocs = []
        for data_source in data_sources:
            ioc_processor = IocProcessor(data_source.alias, data_source.id)
            delimiter = {
                "urlhaus": ",",
                "alienvault": "#",
                "openphish": ",",
            }.get(data_source.alias, None)
            if delimiter is None:
                raise ValueError(f"Unknown data source alias: {data_source.alias}")
            raw_iocs = self.http_gateway.get_csv(data_source.url, delimiter)
            iocs = ioc_processor.process(raw_iocs)
            url_iocs += [UrlIoc(url=ioc.address, data_source=data_source) for ioc in iocs if ioc.type == IocType.URL]
            ip_iocs += [IpIoc(ip=ioc.address, data_source=data_source) for ioc in iocs if ioc.type == IocType.IP]
        self.repository.upsert_url_iocs(url_iocs)
        self.repository.upsert_ip_iocs(ip_iocs)

    @classmethod
    def get_instance(cls):
        """
        Singleton factory method to get service
        :return:
        """
        if not hasattr(cls, "_instance"):
            CommonService._instance = CommonService(CommonRepository.get_instance(), HttpGateway.get_instance())
        return CommonService._instance
