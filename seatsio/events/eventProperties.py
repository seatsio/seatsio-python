class EventProperties:
    def __init__(self, event_key=None, table_booking_config=None, social_distancing_ruleset_key=None, object_categories=None, categories=None):
        if event_key:
            self.eventKey = event_key
        if table_booking_config is not None:
            self.tableBookingConfig = table_booking_config
        if social_distancing_ruleset_key is not None:
            self.socialDistancingRulesetKey = social_distancing_ruleset_key
        if object_categories is not None:
            self.objectCategories = object_categories
        if categories is not None:
            self.categories = categories
