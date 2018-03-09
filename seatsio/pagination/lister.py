from seatsio.pagination.pagedIterator import PagedIterator


class Lister:
    def __init__(self, page_fetcher):
        self.pageFetcher = page_fetcher

    def all(self):
        return PagedIterator(self.pageFetcher)
