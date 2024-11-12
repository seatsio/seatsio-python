from seatsio.events.createSingleEventRequest import CreateSingleEventRequest


class UpdateEventRequest(CreateSingleEventRequest):
    def __init__(self, event_key=None, name=None, date=None, table_booking_config=None,
                 object_categories=None, categories=None, is_in_the_past=None):
        CreateSingleEventRequest.__init__(self, None, event_key, name, date, table_booking_config, object_categories, categories)
        if is_in_the_past is not None:
            self.isInThePast = is_in_the_past
