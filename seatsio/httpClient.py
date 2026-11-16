import re
import time
import uuid
from urllib.parse import quote, urlencode

import jsonpickle
import requests

from seatsio.exceptions import SeatsioException, RateLimitExceededException


UUID_V4 = re.compile(r'\A[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z', re.IGNORECASE)


def handle_error(request, response):
    raise SeatsioException.from_response(request, response)


class HttpClient:
    def __init__(self, base_url, secret_key, workspace_key, max_retries, timeout=10, idempotency_key=None):
        self.base_url = base_url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.max_retries = max_retries
        self.timeout = timeout
        self.idempotency_key = idempotency_key

    def with_idempotency_key(self, idempotency_key):
        if not isinstance(idempotency_key, str) or not UUID_V4.match(idempotency_key):
            raise ValueError("idempotency key %r is not a v4 UUID" % (idempotency_key,))
        return HttpClient(self.base_url, self.secret_key, self.workspace_key, self.max_retries, self.timeout, idempotency_key)

    def withIdempotencyKey(self, idempotency_key):
        return self.with_idempotency_key(idempotency_key)

    def url(self, relative_url, query_params=None, **path_params):
        if query_params is None:
            query_params = {}
        return ApiResource(self.max_retries, self.secret_key, self.workspace_key, self.base_url, relative_url,
                           query_params, self.timeout, self.idempotency_key, **path_params)


class ApiResource:
    def __init__(self, max_retries, secret_key, workspace_key, base_url, relative_url, query_params, timeout, idempotency_key=None, **path_params):
        self.max_retries = max_retries
        self.url = self.__create_full_url(base_url, relative_url, query_params, **path_params)
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.idempotency_key = idempotency_key

    def __create_full_url(self, base_url, relative_url, query_params, **path_params):
        for key in path_params:
            path_params[key] = quote(str(path_params[key]), safe='')
        full_url = base_url + relative_url.format(**path_params)
        if query_params:
            full_url += "?" + urlencode(query_params, True)
        return full_url

    def get(self):
        return GET(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout).execute()

    def get_raw(self):
        return GET(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout).execute_raw()

    def get_as(self, cls):
        return cls(self.get())

    def post(self, body=None):
        if body is None:
            return POST(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).execute()
        else:
            return POST(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).body(body).execute()

    def post_empty_and_return(self, cls):
        return cls(self.post().json())

    def delete(self, body=None):
        if body is None:
            return DELETE(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).execute()
        else:
            return DELETE(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).body(body).execute()

    def put(self, body=None):
        if body is None:
            return PUT(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).execute()
        else:
            return PUT(self.max_retries, self.url, self.secret_key, self.workspace_key, self.timeout, self.idempotency_key).body(body).execute()


class GET:

    def __init__(self, max_retries, url, secret_key, workspace_key, timeout):
        self.http_method = "GET"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.idempotency_key = None

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
            return requests.get(self.url, auth=(self.secret_key, ''), headers=(common_headers(self.workspace_key)), timeout=self.timeout)
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class POST:

    def __init__(self, max_retries, url, secret_key, workspace_key, timeout, idempotency_key=None):
        self.http_method = "POST"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.body_object = None
        self.idempotency_key = idempotency_key if idempotency_key is not None else str(uuid.uuid4())

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
                headers=(common_headers(self.workspace_key, self.idempotency_key)),
                data=json,
                timeout=self.timeout
            )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class DELETE:

    def __init__(self, max_retries, url, secret_key, workspace_key, timeout, idempotency_key=None):
        self.http_method = "DELETE"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.body_object = None
        self.idempotency_key = idempotency_key if idempotency_key is not None else str(uuid.uuid4())

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
                headers=(common_headers(self.workspace_key, self.idempotency_key)),
                data=json,
                timeout=self.timeout
            )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


class PUT:

    def __init__(self, max_retries, url, secret_key, workspace_key, timeout, idempotency_key=None):
        self.http_method = "PUT"
        self.max_retries = max_retries
        self.url = url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.body_object = None
        self.idempotency_key = idempotency_key if idempotency_key is not None else str(uuid.uuid4())

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
            return requests.put(
                self.url,
                auth=(self.secret_key, ''),
                headers=(common_headers(self.workspace_key, self.idempotency_key)),
                data=json,
                timeout=self.timeout
            )
        except Exception as cause:
            raise SeatsioException(self, cause=cause)


def common_headers(workspace_key, idempotency_key=None):
    headers = {
        'X-Workspace-Key': str(workspace_key) if workspace_key else None,
        'X-Client-Lib': 'python'
    }
    if idempotency_key:
        headers['Idempotency-Key'] = idempotency_key
    return headers


def retry(fn, max_retries):
    retry_count = 0
    while True:
        response = fn()
        if not is_retryable(response) or retry_count >= max_retries:
            return response
        else:
            wait_time = (2 ** (retry_count + 2)) / 10.0
            time.sleep(wait_time)
            retry_count += 1


def is_retryable(response):
    if response.status_code == 429:
        return True
    if response.status_code == 409:
        codes = api_error_codes(response)
        return len(codes) > 0 and codes[0] == 'IDEMPOTENCY_KEY_IN_USE'
    return False


def api_error_codes(response):
    if "application/json" not in response.headers.get("content-type", ""):
        return []
    try:
        body = response.json()
    except ValueError:
        return []
    errors = body.get("errors") if isinstance(body, dict) else None
    if not isinstance(errors, list):
        return []
    return [error["code"] for error in errors if isinstance(error, dict) and "code" in error]
