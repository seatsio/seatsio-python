from seatsio.events.createSingleEventRequest import CreateSingleEventRequest


class UpdateSeasonRequest(CreateSingleEventRequest):
    def __init__(self, event_key=None, name=None, table_booking_config=None, object_categories=None, categories=None, for_sale_propagated=None):
        CreateSingleEventRequest.__init__(self, None, event_key, name, None, table_booking_config, object_categories, categories)
        if for_sale_propagated is not None:
            self.forSalePropagated = for_sale_propagated