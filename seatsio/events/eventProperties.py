class EventProperties:
    def __init__(self, event_key=None, name=None, date=None, table_booking_config=None, object_categories=None, categories=None, channels=None, for_sale_config=None):
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
        if channels is not None:
            self.channels = channels
        if for_sale_config is not None:
            self.forSaleConfig = for_sale_config.to_json()
