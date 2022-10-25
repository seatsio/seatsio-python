class ForSaleRequest:
    def __init__(self, objects, area_places, categories):
        if objects:
            self.objects = objects
        if area_places:
            self.areaPlaces = area_places
        if categories:
            self.categories = categories
