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
        self.chartKey = bunch.chartKey
        self.bookWholeTables = bunch.bookWholeTables
        self.forSaleConfig = getattr(bunch, "forSaleConfig", None)
        self.createdOn = datetime.strptime(bunch.createdOn, "%Y-%m-%dT%H:%M:%S.%fZ")
        updated_on = getattr(bunch, "updatedOn", None)
        if updated_on:
            self.updatedOn = datetime.strptime(updated_on, "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.updatedOn = None


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
        # TODO extraData


class StatusChange:
    def __init__(self, dict):
        bunch = bunchify(dict)
        self.id = bunch.id
        self.status = bunch.status
        self.date = datetime.strptime(bunch.date, "%Y-%m-%dT%H:%M:%S.%fZ")
        self.objectLabel = bunch.objectLabel
        self.eventId = bunch.eventId
        self.extraData = getattr(bunch, "extraData", None)


class ObjectProperties:
    def __init__(self, object_id, extra_data=None):
        if extra_data is None:
            extra_data = {}
        self.extraData = extra_data
        self.objectId = object_id
