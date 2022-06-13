from seatsio.events.channelsRequests import ReplaceChannelsRequest, AssignObjectsToChannelsRequest


class ChannelsClient:
    def __init__(self, http_client):
        self.http_client = http_client

    def add(self):
        return 'TODO'

    def remove(self):
        return 'TODO'

    def update(self):
        return 'TODO'

    def add_objects(self):
        return 'TODO'

    def remove_objects(self):
        return 'TODO'

    def replace(self, event_key, channels):
        self.http_client \
            .url('/events/{event_key}/channels/update', event_key=event_key) \
            .post(ReplaceChannelsRequest(channels))

    def set_objects(self, event_key, channels):
        self.http_client \
            .url('/events/{event_key}/channels/assign-objects', event_key=event_key) \
            .post(AssignObjectsToChannelsRequest(channels))
