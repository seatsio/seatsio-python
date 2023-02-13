from seatsio.events.channelsRequests import ReplaceChannelsRequest, AssignObjectsToChannelsRequest, AddChannelRequest, \
    EditObjectsForChannelRequest, UpdateChannelRequest


class ChannelsClient:
    def __init__(self, http_client):
        self.http_client = http_client

    def add(self, event_key, channel_key, channel_name, channel_color, index=None, objects=None):
        self.http_client \
            .url('/events/{key}/channels', key=event_key) \
            .post(AddChannelRequest(channel_key, channel_name, channel_color, index, objects))

    def add_multiple(self, event_key, channels_properties):
        self.http_client \
            .url('/events/{key}/channels', key=event_key) \
            .post(channels_properties)

    def remove(self, event_key, channel_key):
        self.http_client \
            .url('/events/{event_key}/channels/{channel_key}', event_key=event_key, channel_key=channel_key) \
            .delete()

    def update(self, event_key, channel_key, name=None, color=None, objects=None):
        self.http_client \
            .url("/events/{event_key}/channels/{channel_key}", event_key=event_key, channel_key=channel_key) \
            .post(UpdateChannelRequest(name, color, objects))

    def add_objects(self, event_key, channel_key, objects):
        self.http_client \
            .url("/events/{event_key}/channels/{channel_key}/objects", event_key=event_key, channel_key=channel_key) \
            .post(EditObjectsForChannelRequest(objects))

    def remove_objects(self, event_key, channel_key, objects):
        self.http_client \
            .url("/events/{event_key}/channels/{channel_key}/objects", event_key=event_key, channel_key=channel_key) \
            .delete(EditObjectsForChannelRequest(objects))

    def replace(self, event_key, channels):
        self.http_client \
            .url('/events/{event_key}/channels/update', event_key=event_key) \
            .post(ReplaceChannelsRequest(channels))

    def set_objects(self, event_key, channels):
        self.http_client \
            .url('/events/{event_key}/channels/assign-objects', event_key=event_key) \
            .post(AssignObjectsToChannelsRequest(channels))
