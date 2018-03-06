from urllib2 import URLError

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
        response = self.__try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def __try_execute(self):
        try:
            return unirest.get(self.url, auth=self.auth)
        except Exception:
            raise SeatsioException(self)
