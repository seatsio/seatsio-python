import urllib

import jsonpickle
import unirest

from seatsio.exceptions import SeatsioException


class HttpClient:
    def __init__(self, base_url, secret_key):
        self.baseUrl = base_url
        self.secretKey = secret_key

    def url(self, relative_url, query_params=None, **path_params):
        if query_params is None:
            query_params = {}
        return ApiResource(self.secretKey, self.baseUrl, relative_url, query_params, **path_params)


class ApiResource:
    def __init__(self, secret_key, base_url, relative_url, query_params, **path_params):
        self.url = self.__create_full_url(base_url, relative_url, query_params, **path_params)
        self.secretKey = secret_key

    # TODO refactor into URL class
    def __create_full_url(self, base_url, relative_url, query_params, **path_params):
        for key in path_params:
            path_params[key] = urllib.quote(str(path_params[key]), safe='')
        full_url = base_url + relative_url.format(**path_params)
        if query_params:
            full_url += "?" + urllib.urlencode(query_params)
        return full_url

    def get(self):
        return GET(self.url, self.secretKey).execute()

    def get_as(self, cls):
        return cls(self.get().body)

    def post(self, body=None):
        if body is None:
            return POST(self.url, self.secretKey).execute()
        else:
            return POST(self.url, self.secretKey).body(body).execute()

    def post_empty_and_return(self, cls):
        return cls(self.post().body)

    def delete(self):
        return DELETE(self.url, self.secretKey).execute()


class HttpRequest:
    def __init__(self, method, full_url, secret_key):
        self.httpMethod = method
        self.url = full_url
        self.secret_key = secret_key

    def execute(self):
        response = self.try_execute()
        if response.code >= 400:
            raise SeatsioException(self, response)
        else:
            return response

    def try_execute(self):
        raise NotImplementedError


class GET(HttpRequest):

    def __init__(self, url, secret_key):
        HttpRequest.__init__(self, "GET", url, secret_key)

    def try_execute(self):
        try:
            return unirest.get(self.url, auth=(self.secret_key, ''))
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST(HttpRequest):

    def __init__(self, url, secret_key):
        HttpRequest.__init__(self, "POST", url, secret_key)
        self.bodyObject = None

    def body(self, body):
        self.bodyObject = body
        return self

    def try_execute(self):
        try:
            if self.bodyObject:
                json = jsonpickle.encode(self.bodyObject, unpicklable=False)
                return unirest.post(
                    url=self.url,
                    auth=(self.secret_key, ''),
                    headers={"Accept": "application/json"},
                    params=json
                )
            else:
                return unirest.post(
                    url=self.url,
                    auth=(self.secret_key, '')
                )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class DELETE(HttpRequest):

    def __init__(self, url, secret_key):
        HttpRequest.__init__(self, "DELETE", url, secret_key)

    def try_execute(self):
        try:
            return unirest.delete(self.url, auth=(self.secret_key, ''))
        except Exception as cause:
            raise SeatsioException(self, cause=cause)
