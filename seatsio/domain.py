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
        self.events = None # TODO
        self.tags = [] #TODO
        self.archived = getattr(bunch, 'archived', False)

