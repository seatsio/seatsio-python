class Page:

    def __init__(self, items, next_page_starts_after, previous_page_ends_before):
        self.next_page_starts_after = next_page_starts_after
        self.previous_page_ends_before = previous_page_ends_before
        self.items = items

    def set_next_page_starts_after(self, next_page_starts_after):
        self.next_page_starts_after = next_page_starts_after

    def set_previous_page_ends_before(self, previous_page_ends_before):
        self.previous_page_ends_before = previous_page_ends_before

    @classmethod
    def from_response(cls, response, clazz):
        # TODO cleanup
        items = response.body["items"]
        next_page_starts_after = response.body.get("next_page_starts_after", None)
        if (next_page_starts_after):
            next_page_starts_after = int(next_page_starts_after)
        previous_page_ends_before = response.body.get("previous_page_ends_before", None)
        if (previous_page_ends_before):
            previous_page_ends_before = int(previous_page_ends_before)
        typed_items = []
        for item in items:
            typed_items.append(clazz(item))
        return Page(typed_items, next_page_starts_after, previous_page_ends_before)
