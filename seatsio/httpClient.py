import jsonpickle
import unirest

from seatsio.exceptions import SeatsioException


class GET:
    def __init__(self, url):
        self.httpMethod = "GET"
        self.url = url

    def basic_auth(self, username, password):
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
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST:
    def __init__(self, url):
        self.httpMethod = "POST"
        self.url = url
        self.bodyObject = None

    def basic_auth(self, username, password):
        self.auth = (username, password)
        return self

    def body(self, body):
        self.bodyObject = body
        return self

    def execute(self):
        response = self.__try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def __try_execute(self):
        try:
            if self.bodyObject:
                json = jsonpickle.encode(self.bodyObject, unpicklable=False)
                return unirest.post(
                    url=self.url,
                    auth=self.auth,
                    headers={"Accept": "application/json"},
                    params=json
                )
            else:
                return unirest.post(
                    url=self.url,
                    auth=self.auth
                )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)
