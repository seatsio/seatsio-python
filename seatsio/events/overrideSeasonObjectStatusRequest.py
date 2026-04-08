class OverrideSeasonObjectStatusRequest:
    def __init__(self, objects, season=None):
        self.objects = objects
        if season is not None:
            self.season = season
