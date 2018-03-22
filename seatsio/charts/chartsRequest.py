
class ChartRequest:

    def __init__(self, name=None, venue_type=None, categories=None):
        if name:
            self.name = name
        if venue_type:
            self.venueType = venue_type
        if categories:
            self.categories = categories
