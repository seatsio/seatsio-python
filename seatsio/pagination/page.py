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
        next_page_starts_after = cls.get_value(response, "next_page_starts_after")
        previous_page_ends_before = cls.get_value(response, "previous_page_ends_before")
        items = cls.map_items(clazz, response)
        return Page(items, next_page_starts_after, previous_page_ends_before)

    @classmethod
    def get_value(cls, response, param_name):
        int_value = response.get(param_name, None)
        if int_value:
            int_value = int(int_value)
        return int_value

    @classmethod
    def map_items(cls, clazz, response):
        typed_items = []
        for item in response["items"]:
            typed_items.append(clazz(item))
        return typed_items
