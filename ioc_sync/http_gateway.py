import csv
from codecs import iterdecode
from contextlib import closing

import requests


class HttpGateway:
    def __init__(self):
        # we could add headers config, proxies and such here
        pass

    @classmethod
    def get_instance(cls):
        if not hasattr(cls, "_instance"):
            HttpGateway._instance = HttpGateway()
        return HttpGateway._instance

    def get_csv(self, url, delimiter=','):
        with closing(requests.get(url, stream=True)) as r:
            reader = csv.reader(iterdecode((line for line in r.iter_lines() if not line.startswith(b'#')), 'utf-8'), delimiter=delimiter)
            return [row for row in reader]
