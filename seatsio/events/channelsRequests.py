class ReplaceChannelsRequest:
    def __init__(self, channels):
        if channels:
            self.channels = [c.to_json() for c in channels]


class AssignObjectsToChannelsRequest:
    def __init__(self, channel_config):
        if channel_config:
            self.channelConfig = channel_config


class AddChannelRequest:
    def __init__(self, key, name, color, index, objects, area_places):
        self.key = key
        self.name = name
        self.color = color
        if index:
            self.index = index
        if objects:
            self.objects = objects
        if area_places is not None:
            self.areaPlaces = area_places


class EditObjectsForChannelRequest:
    def __init__(self, objects=None, area_places=None):
        if objects is not None:
            self.objects = objects
        if area_places is not None:
            self.areaPlaces = area_places

class UpdateChannelRequest:
    def __init__(self, name, color, objects, area_places):
        if name:
            self.name = name
        if color:
            self.color = color
        if objects:
            self.objects = objects
        if area_places is not None:
            self.areaPlaces = area_places
