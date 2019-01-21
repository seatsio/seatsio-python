class CreateMultipleEventsRequest:
    def __init__(self, chart_key, events_properties):
        if chart_key:
            self.chartKey = chart_key
        if events_properties:
            self.events = events_properties
