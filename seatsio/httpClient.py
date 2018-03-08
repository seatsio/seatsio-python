import jsonpickle
import unirest

from seatsio.exceptions import SeatsioException


class HttpClient:
    def __init__(self, base_url, secret_key):
        self.baseUrl = base_url
        self.secretKey = secret_key

    def get(self, url):
        return GET(self.baseUrl + url).auth(self.secretKey, '')

    def post(self, url):
        return POST(self.baseUrl + url).auth(self.secretKey, '')


class GET:
    def __init__(self, url):
        self.httpMethod = "GET"
        self.url = url

    def auth(self, username, password):
        self.credentials = (username, password)
        return self

    def execute(self):
        response = self.__try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def __try_execute(self):
        try:
            return unirest.get(self.url, auth=self.credentials)
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST:
    def __init__(self, url):
        self.httpMethod = "POST"
        self.url = url
        self.bodyObject = None

    def auth(self, username, password):
        self.credentials = (username, password)
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
                    auth=self.credentials,
                    headers={"Accept": "application/json"},
                    params=json
                )
            else:
                return unirest.post(
                    url=self.url,
                    auth=self.credentials
                )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)
