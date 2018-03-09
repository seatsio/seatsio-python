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


class Subaccount:

    def __init__(self, dict):
        bunch = bunchify(dict)
        self.id = bunch.id
        self.secretKey = bunch.secretKey
        self.designerKey = bunch.designerKey
        self.publicKey = bunch.publicKey
        self.name = getattr(bunch, 'name', None)
        self.active = bunch.active
