from seatsio.pagination.page import Page


class PageFetcher:
    def __init__(self, http_client, url):
        self.url = url
        self.httpClient = http_client
        self.page_size = None

    def fetch_after(self, after_id=None):
        if after_id:
            return self.__fetch(start_after_id=after_id)
        else:
            return self.__fetch()

    def fetch_before(self, before_id=None):
        if before_id:
            return self.__fetch(end_before_id=before_id)
        else:
            return self.__fetch()

    def __fetch(self, **query_params):
        if self.page_size:
            query_params["limit"] = self.page_size
        response = self.httpClient.url(self.url, **query_params).get()
        return Page(response.body["items"])
