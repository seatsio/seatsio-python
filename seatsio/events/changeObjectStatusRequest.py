from past.builtins import basestring

from seatsio.events.objectProperties import ObjectProperties


class ChangeObjectStatusRequest:
    def __init__(self, type, object_or_objects, status, hold_token, order_id, event_key_or_keys, keep_extra_data, ignore_channels, channel_keys,
                 allowed_previous_statuses=None, rejected_previous_statuses=None, resale_listing_id=None):
        self.objects = self.__normalize_objects(object_or_objects)
        if type is not None:
            self.type = type
        if status is not None:
            self.status = status
        if hold_token:
            self.holdToken = hold_token
        if order_id:
            self.orderId = order_id
        if isinstance(event_key_or_keys, basestring):
            self.events = [event_key_or_keys]
        else:
            self.events = event_key_or_keys
        if keep_extra_data is not None:
            self.keepExtraData = keep_extra_data
        if ignore_channels is not None:
            self.ignoreChannels = ignore_channels
        if channel_keys is not None:
            self.channelKeys = channel_keys
        if allowed_previous_statuses is not None:
            self.allowedPreviousStatuses = allowed_previous_statuses
        if rejected_previous_statuses is not None:
            self.rejectedPreviousStatuses = rejected_previous_statuses
        if resale_listing_id is not None:
            self.resaleListingId = resale_listing_id

    def __normalize_objects(self, object_or_objects):
        if isinstance(object_or_objects, list):
            if len(object_or_objects) == 0:
                return []
            if isinstance(object_or_objects[0], ObjectProperties):
                return object_or_objects
            if isinstance(object_or_objects[0], basestring):
                result = []
                for o in object_or_objects:
                    result.append(ObjectProperties(o))
                return result
            else:
                raise Exception("Unsupported type " + str(type(object_or_objects[0])))
        return self.__normalize_objects([object_or_objects])
