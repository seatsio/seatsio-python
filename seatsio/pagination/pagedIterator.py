class PagedIterator:
    def __init__(self, page_fetcher):
        self.current_page = None
        self.index_in_current_page = 0
        self.pageFetcher = page_fetcher

    def __iter__(self):
        return self

    def __getitem__(self, index):
        return self.__get_current_page().items[index]

    def next(self):
        try:
            result = self.__get_current_page().items[self.index_in_current_page]
        except IndexError:
            raise StopIteration
        self.index_in_current_page += 1
        return result

    def __next__(self):
        return self.next()

    def current(self):
        return self.__getitem__(self.index_in_current_page)

    def __get_current_page(self):
        if not self.current_page:
            self.current_page = self.pageFetcher.fetch_after(None)
        elif self.__next_page_must_be_fetched():
            self.current_page = self.pageFetcher.fetch_after(self.current_page.next_page_starts_after)
            self.index_in_current_page = 0
        return self.current_page

    def __next_page_must_be_fetched(self):
        index_is_beyond_current_page = self.index_in_current_page >= len(self.current_page.items)
        next_page_exists = self.current_page.next_page_starts_after is not None
        return index_is_beyond_current_page and next_page_exists
