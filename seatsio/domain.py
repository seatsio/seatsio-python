from datetime import datetime

from bunch import bunchify


class Chart:

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.id = bunch.id
        self.key = bunch.key
        self.status = bunch.status
        self.name = bunch.name
        self.publishedVersionThumbnailUrl = bunch.publishedVersionThumbnailUrl
        self.draftVersionThumbnailUrl = getattr(bunch, 'draftVersionThumbnailUrl', None)
        self.events = getattr(bunch, 'events', None)
        self.tags = bunch.tags
        self.archived = getattr(bunch, 'archived', False)


class Event:

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.id = bunch.id
        self.key = bunch.key


class Subaccount:

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.id = bunch.id
        self.secretKey = bunch.secretKey
        self.designerKey = bunch.designerKey
        self.publicKey = bunch.publicKey
        self.name = getattr(bunch, 'name', None)
        self.active = bunch.active


class HoldToken:

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.hold_token = bunch.holdToken
        self.expires_at = datetime.strptime(bunch.expiresAt, "%Y-%m-%dT%H:%M:%S.%fZ")


class ObjectStatus:
    FREE = "free"
    BOOKED = "booked"
    HELD = "reservedByToken"

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.status = bunch.status
        self.hold_token = getattr(bunch, "holdToken", None)
        self.order_id = getattr(bunch, "orderId", None)
        self.ticket_type = getattr(bunch, "ticketType", None)
        self.quantity = getattr(bunch, "quantity", None)
        # TODO extradata
