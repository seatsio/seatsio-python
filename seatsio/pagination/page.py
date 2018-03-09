class Page:

    def __init__(self, items):
        self.next_page_starts_after = None
        self.previous_page_ends_before = None
        self.items = items

    def set_next_page_starts_after(self, next_page_starts_after):
        self.next_page_starts_after = next_page_starts_after

    def set_previous_page_ends_before(self, previous_page_ends_before):
        self.previous_page_ends_before = previous_page_ends_before

    def __iter__(self):
        return self.items.__iter__()

    def __len__(self):
        return len(self.items)
