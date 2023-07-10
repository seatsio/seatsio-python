class EventProperties:
    def __init__(self, event_key=None, name=None, date=None, table_booking_config=None, object_categories=None, categories=None):
        if event_key:
            self.eventKey = event_key
        if name:
            self.name = name
        if date:
            self.date = date
        if table_booking_config is not None:
            self.tableBookingConfig = table_booking_config
        if object_categories is not None:
            self.objectCategories = object_categories
        if categories is not None:
            self.categories = categories
