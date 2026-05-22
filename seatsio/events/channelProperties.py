class ChannelCreationParams:
    def __init__(self, key, name, color, index=None, objects=None, area_places=None):
        self.key = key
        self.name = name
        self.color = color
        self.index = index
        self.objects = objects
        self.area_places = area_places

    def to_json(self):
        json = {
            'key': self.key,
            'name': self.name,
            'color': self.color,
        }
        if self.index is not None:
            json['index'] = self.index
        if self.objects is not None:
            json['objects'] = self.objects
        if self.area_places is not None:
            json['areaPlaces'] = self.area_places
        return json

