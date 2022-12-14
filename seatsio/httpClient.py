import time

import jsonpickle
import requests
from six.moves.urllib.parse import quote, urlencode

from seatsio.exceptions import SeatsioException, RateLimitExceededException


def handle_error(request, response):
    if response.status_code == 429:
        raise RateLimitExceededException(request, response)
    else:
        raise SeatsioException(request, response)


class HttpClient:
    def __init__(self, base_url, secret_key, workspace_key, max_retries):
        self.base_url = base_url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.max_retries = max_retries

    def url(self, relative_url, query_params=None, **path_params):
        if query_params is None:
            query_params = {}
        return ApiResource(self.max_retries, self.secret_key, self.workspace_key, self.base_url, relative_url,
                           query_params, **path_params)


class ApiResource:
    def __init__(self, max_retries, secret_key, workspace_key, base_url, relative_url, query_params, **path_params):
        self.max_retries = max_retries
        self.url = self.__create_full_url(base_url, relative_url, query_params, **path_params)
        self.secret_key = secret_key
        self.workspace_key = workspace_key

    def __create_full_url(self, base_url, relative_url, query_params, **path_params):
        for key in path_params:
            path_params[key] = quote(str(path_params[key]), safe='')
        full_url = base_url + relative_url.format(**path_params)
        if query_params:
            full_url += "?" + urlencode(query_params, True)
        return full_url

    def get(self):
        return GET(self.max_retries, self.url, self.secret_key, self.workspace_key).execute()

    def get_raw(self):
        return GET(self.max_retries, self.url, self.secret_key, self.workspace_key).execute_raw()

    def get_as(self, cls):
        return cls(self.get())

    def post(self, body=None):
        if body is None:
            return POST(self.max_retries, self.url, self.secret_key, self.workspace_key).execute()
        else:
            return POST(self.max_retries, self.url, self.secret_key, self.workspace_key).body(body).execute()

    def post_empty_and_return(self, cls):
        return cls(self.post().json())

    def delete(self, body=None):
        if body is None:
            return DELETE(self.max_retries, self.url, self.secret_key, self.workspace_key).execute()
        else:
            return DELETE(self.max_retries, self.url, self.secret_key, self.workspace_key).body(body).execute()


class GET:

    def __init__(self, max_retries, url, secret_key, workspace_key):
        self.http_method = "GET"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key

    def execute(self):
        response = retry(self.try_execute, self.max_retries)
        if response.status_code >= 400:
            handle_error(self, response)
        else:
            return response.json()

    def execute_raw(self):
        response = retry(self.try_execute, self.max_retries)
        if response.status_code >= 400:
            handle_error(self, response)
        else:
            return response.content

    def try_execute(self):
        try:
            return requests.get(self.url, auth=(self.secret_key, ''), headers=(common_headers(self.workspace_key)))
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST:

    def __init__(self, max_retries, url, secret_key, workspace_key):
        self.http_method = "POST"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.body_object = None

    def body(self, body):
        self.body_object = body
        return self

    def execute(self):
        response = retry(self.try_execute, self.max_retries)
        if response.status_code >= 400:
            handle_error(self, response)
        else:
            return response

    def try_execute(self):
        try:
            json = jsonpickle.encode(self.body_object, unpicklable=False)
            return requests.post(
                url=self.url,
                auth=(self.secret_key, ''),
                headers=(common_headers(self.workspace_key)),
                data=json
            )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class DELETE:

    def __init__(self, max_retries, url, secret_key, workspace_key):
        self.http_method = "DELETE"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.body_object = None

    def body(self, body):
        self.body_object = body
        return self

    def execute(self):
        response = retry(self.try_execute, self.max_retries)
        if response.status_code >= 400:
            handle_error(self, response)
        else:
            return response

    def try_execute(self):
        try:
            json = jsonpickle.encode(self.body_object, unpicklable=False)
            return requests.delete(
                self.url,
                auth=(self.secret_key, ''),
                headers=(common_headers(self.workspace_key)),
                data=json
            )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


def common_headers(workspace_key):
    return {
        'X-Workspace-Key': str(workspace_key) if workspace_key else None,
        'X-Client-Lib': 'python'
    }


def retry(fn, max_retries):
    retry_count = 0
    while True:
        response = fn()
        if response.status_code != 429 or retry_count >= max_retries:
            return response
        else:
            wait_time = (2 ** (retry_count + 2)) / 10.0
            time.sleep(wait_time)
            retry_count += 1
