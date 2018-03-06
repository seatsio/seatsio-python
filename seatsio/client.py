import unirest

from seatsio.exceptions import SeatsioException


class SeatsioClient:

    def __init__(self, secret_key, base_url):
        self.secretKey = secret_key
        self.baseUrl = base_url

    def charts(self):
        return Charts(self.secretKey, self.baseUrl)


class Charts:

    def __init__(self, secret_key, base_url):
        self.secretKey = secret_key
        self.baseUrl = base_url

    def retrieve(self, chart_key):
        url = self.baseUrl + "/charts/" + chart_key
        response = Get(url).basicAuth(self.secretKey, '').execute()
        # TODO create chart object
        return response


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
