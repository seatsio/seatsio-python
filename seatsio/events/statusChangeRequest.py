class StatusChangeRequest:
    def __init__(self, event_key, object_or_objects, status, hold_token=None, order_id=None, keep_extra_data=None, ignore_channels=None, channel_keys=None, allowed_previous_statuses=None, rejected_previous_statuses=None):
        self.event_key = event_key
        self.object_or_objects = object_or_objects
        self.status = status
        self.hold_token = hold_token
        self.order_id = order_id
        self.keep_extra_data = keep_extra_data
        self.ignore_channels = ignore_channels
        self.channel_keys = channel_keys
        self.allowed_previous_statuses = allowed_previous_statuses
        self.rejected_previous_statuses = rejected_previous_statuses
