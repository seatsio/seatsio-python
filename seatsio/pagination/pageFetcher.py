from seatsio.pagination.page import Page


class PageFetcher:
    def __init__(self, http_client, url, cls):
        self.url = url
        self.httpClient = http_client
        self.page_size = None
        self.query_params = {}
        self.cls = cls

    def fetch_after(self, after_id=None):
        if after_id:
            self.set_query_param("start_after_id", after_id)
        return self.__fetch()

    def fetch_before(self, before_id=None):
        if before_id:
            self.set_query_param("end_before_id", before_id)
        return self.__fetch()

    def __fetch(self):
        if self.page_size:
            self.set_query_param("limit", self.page_size)
        items = self.httpClient.url(self.url, self.query_params).get().body["items"]
        typed_items = []
        for item in items:
            typed_items.append(self.cls(item))
        return Page(typed_items)

    def set_query_param(self, key, value):
        self.query_params[key] = value
