class Chart:

    def __init__(self, id, key, tags):
        self.id = id
        self.key = key
        self.tags = tags

    @classmethod
    def fromJson(cls, body):
        return Chart(
            id=body["id"],
            key=body["key"],
            tags = body["tags"]
        )
