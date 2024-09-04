class ChangeBestAvailableObjectStatusRequest:
    def __init__(self, number, categories, zone, extra_data, ticket_types, status, hold_token, order_id, keep_extra_data, ignore_channels, channel_keys, try_to_prevent_orphan_seats, accessible_seats):
        best_available = {"number": number}
        if categories:
            best_available["categories"] = categories
        if zone:
            best_available["zone"] = zone
        if extra_data:
            best_available["extraData"] = extra_data
        if ticket_types:
            best_available["ticketTypes"] = ticket_types
        if try_to_prevent_orphan_seats is not None:
            best_available["tryToPreventOrphanSeats"] = try_to_prevent_orphan_seats
        if accessible_seats is not None:
            best_available["accessibleSeats"] = accessible_seats
        self.bestAvailable = best_available
        self.status = status
        if hold_token:
            self.holdToken = hold_token
        if order_id:
            self.orderId = order_id
        if keep_extra_data is not None:
            self.keepExtraData = keep_extra_data
        if ignore_channels is not None:
            self.ignoreChannels = ignore_channels
        if channel_keys is not None:
            self.channelKeys = channel_keys
