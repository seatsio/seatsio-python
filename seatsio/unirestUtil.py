import unirest

from seatsio.exceptions import SeatsioException


class Get:
    def __init__(self, url):
        self.httpMethod = "GET"
        self.url = url

    def basicAuth(self, username, password):
        self.auth = (username, password)
        return self

    def execute(self):
        # TODO bver catch RuntimeErrors as well
        response = unirest.get(self.url, auth=self.auth)
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response
