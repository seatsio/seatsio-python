from seatsio.pagination.pagedIterator import PagedIterator

class Lister:
    def __init__(self, page_fetcher):
        self.pageFetcher = page_fetcher

    def list(self):
        return PagedIterator(self.pageFetcher)

    def first_page(self):
        return self.pageFetcher.fetch_after(None)

    def page_after(self, id):
        return self.pageFetcher.fetch_after(id)

    def page_before(self, id):
        return self.pageFetcher.fetch_before(id)

    def set_page_size(self, page_size):
        self.pageFetcher.set_page_size(page_size)
        return self
