class ReplaceChannelsRequest:
    def __init__(self, channels):
        if channels:
            self.channels = channels


class AssignObjectsToChannelsRequest:
    def __init__(self, channel_config):
        if channel_config:
            self.channelConfig = channel_config


class AddChannelRequest:
    def __init__(self, key, name, color, index, objects):
        self.key = key
        self.name = name
        self.color = color
        if index:
            self.index = index
        if objects:
            self.objects = objects


class EditObjectsForChannelRequest:
    def __init__(self, objects):
        self.objects = objects

class UpdateChannelRequest:
    def __init__(self, name, color, objects):
        if name:
            self.name = name
        if color:
            self.color = color
        if objects:
            self.objects = objects
