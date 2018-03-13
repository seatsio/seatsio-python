from seatsio.pagination.pagedIterator import PagedIterator


class Lister:
    def __init__(self, page_fetcher):
        self.pageFetcher = page_fetcher

    def all(self):
        return PagedIterator(self.pageFetcher)

    def page_after(self, id):
        return self.pageFetcher.fetch_after(id)

    def set_filter(self, filter_value):
        self.pageFetcher.set_query_param("filter", filter_value)
        return self

    def set_tag(self, tag_value):
        self.pageFetcher.set_query_param("tag", tag_value)
        return self

    def set_expand_events(self):
        self.pageFetcher.set_query_param("expand", "events")
        return self

    def set_page_size(self, page_size):
        self.pageFetcher.set_page_size(page_size)
        return self
