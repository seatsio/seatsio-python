class ChannelProperties:
    def __init__(self, key=None, name=None, color=None, index=None, objects=None, area_places=None):
        if key is not None:
            self.key = key
        if name is not None:
            self.name = name
        if color is not None:
            self.color = color
        if index is not None:
            self.index = index
        if objects is not None:
            self.objects = objects
        if area_places is not None:
            self.areaPlaces = area_places
