class CreateChartRequest:

    def __init__(self, name, venue_type, categories):
        if name:
            self.name = name
        if venue_type:
            self.venueType = venue_type
        if categories:
            self.categories = categories
