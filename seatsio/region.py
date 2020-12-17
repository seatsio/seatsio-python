class Region:
    def __init__(self, url):
        self.url = url

    @classmethod
    def US(cls):
        return Region(Region.url_for_id("us"))

    @classmethod
    def EU(cls):
        return Region(Region.url_for_id("eu"))

    @classmethod
    def url_for_id(cls, id):
        return "https://api-" + id + ".seatsio.net"
