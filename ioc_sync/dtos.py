import enum
from dataclasses import dataclass
from ipaddress import ip_address
from urllib.parse import urlparse


class IocType(enum.Enum):
    IP = "ip"
    URL = "url"


@dataclass
class IocDto:
    address: str
    data_source_id: int
    type: IocType


class IocMapper:
    @staticmethod
    def ioc_type(address):
        try:
            result = urlparse(address)
            if all([result.scheme, result.netloc]):
                return IocType.URL
        except ValueError:
            pass
        try:
            result = ip_address(address)
            if result:
                return IocType.IP
        except ValueError:
            pass
        raise ValueError(f"Invalid ioc address {address}")

    def __init__(self, data_source_id: int):
        self.data_source_id = data_source_id

    def map(self, raw_iocs: list) -> list[IocDto]:
        raise NotImplementedError


class UrlhausMapper(IocMapper):
    def map(self, raw_iocs: list[tuple]) -> list[IocDto]:
        return [
            IocDto(data_source_id=self.data_source_id, address=ioc[2], type=self.ioc_type(ioc[2])) for ioc in raw_iocs]


class AlienvaultMapper(IocMapper):
    def map(self, raw_iocs: list[tuple]) -> list[IocDto]:
        return [
            IocDto(data_source_id=self.data_source_id, address=ioc[0], type=self.ioc_type(ioc[0])) for ioc in raw_iocs]


class OpenphishMapper(IocMapper):
    def map(self, raw_iocs: list[tuple]) -> list[IocDto]:
        return [
            IocDto(data_source_id=self.data_source_id, address=ioc[0], type=self.ioc_type(ioc[0])) for ioc in raw_iocs]


class IocProcessor:
    def __init__(self, alias: str, data_source_id: int):
        if alias == 'urlhaus':
            self.mapper = UrlhausMapper(data_source_id)
        elif alias == 'alienvault':
            self.mapper = AlienvaultMapper(data_source_id)
        elif alias == 'openphish':
            self.mapper = OpenphishMapper(data_source_id)
        else:
            raise ValueError(f"Unknown alias {alias}")

    def process(self, raw_iocs: list):
        return self.mapper.map(raw_iocs)
