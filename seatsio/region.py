class Region:
    def __init__(self, url):
        self.url = url

    @classmethod
    def EU(cls):
        return Region(Region.url_for_id("eu"))

    @classmethod
    def NA(cls):
        return Region(Region.url_for_id("na"))

    @classmethod
    def SA(cls):
        return Region(Region.url_for_id("sa"))

    @classmethod
    def OC(cls):
        return Region(Region.url_for_id("oc"))

    @classmethod
    def url_for_id(cls, id):
        return "https://api-" + id + ".seatsio.net"
