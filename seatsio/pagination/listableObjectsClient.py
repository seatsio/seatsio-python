from seatsio.pagination.lister import Lister
from seatsio.pagination.pageFetcher import PageFetcher


class ListableObjectsClient:

    def __init__(self, http_client, cls, relative_url):
        self.http_client = http_client
        self.cls = cls
        self.relative_url = relative_url

    def list(self):
        return self.__lister().list()

    def __lister(self):
        return Lister(PageFetcher(self.cls, self.http_client, self.relative_url))

    def list_first_page(self, page_size=None, filter=None):
        return self.__lister().first_page(page_size, filter)

    def list_page_after(self, after_id, page_size=None, filter=None):
        return self.__lister().page_after(after_id, page_size, filter)

    def list_page_before(self, before_id, page_size=None, filter=None):
        return self.__lister().page_before(before_id, page_size, filter)
