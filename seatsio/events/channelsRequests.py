class UpdateChannelsRequest:
    def __init__(self, channels):
        if channels:
            self.channels = channels


class AssignObjectsToChannelsRequest:
    def __init__(self, channelConfig):
        if channelConfig:
            self.channelConfig = channelConfig
