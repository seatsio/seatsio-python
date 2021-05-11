from seatsio.pagination.pagedIterator import PagedIterator


class Lister:
    def __init__(self, page_fetcher):
        self.pageFetcher = page_fetcher

    def list(self, filter=None):
        if filter is not None:
            self.pageFetcher.set_query_param("filter", filter)

        return PagedIterator(self.pageFetcher)

    def first_page(self, page_size=None, filter=None):
        if filter is not None:
            self.pageFetcher.set_query_param("filter", filter)

        return self.pageFetcher.set_page_size(page_size).fetch_after(None)

    def page_after(self, id, page_size=None, filter=None):
        if filter is not None:
            self.pageFetcher.set_query_param("filter", filter)

        return self.pageFetcher.set_page_size(page_size).fetch_after(id)

    def page_before(self, id, page_size=None, filter=None):
        if filter is not None:
            self.pageFetcher.set_query_param("filter", filter)

        return self.pageFetcher.set_page_size(page_size).fetch_before(id)
