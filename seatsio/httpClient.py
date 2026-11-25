import re
import threading
import time
import uuid
from enum import Enum
from urllib.parse import quote, urlencode

import jsonpickle
import requests
from urllib3.exceptions import NewConnectionError

from seatsio.errorResponse import is_idempotency_key_in_use
from seatsio.exceptions import SeatsioException
from seatsio.idempotencyKeyStatus import IdempotencyKeyStatus, IDEMPOTENCY_KEY_HEADER

UUID_V4 = re.compile(r'\A[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}\Z', re.IGNORECASE)

SAFE_METHODS = frozenset(["GET", "HEAD", "OPTIONS", "TRACE"])

# The server keeps an Idempotency-Key for 10 minutes. Once an attempt of a write may have reached the server, every
# retry must start well within that time, otherwise the key may have expired and the retry runs as a new request.
RETRY_WINDOW_SECONDS = 5 * 60


class SystemClock:

    @staticmethod
    def now():
        return time.monotonic()

    @staticmethod
    def sleep(seconds):
        time.sleep(seconds)


class HttpClient:
    def __init__(self, base_url, secret_key, workspace_key, max_retries, timeout=10, idempotency_key=None,
                 clock=None):
        self.base_url = base_url
        self.secret_key = secret_key
        self.workspace_key = workspace_key
        self.timeout = timeout
        self.idempotency_key = idempotency_key
        self._state = _SharedState(max_retries, clock or SystemClock())

    @property
    def max_retries(self):
        """
        The number of times the client retries a request after the first attempt, whatever the reason. Shared with
        the copies made by with_idempotency_key().
        """
        return self._state.max_retries

    @max_retries.setter
    def max_retries(self, max_retries):
        self._state.max_retries = max_retries

    def with_idempotency_key(self, idempotency_key):
        if not isinstance(idempotency_key, str) or not UUID_V4.match(idempotency_key):
            raise ValueError("idempotency key %r is not a v4 UUID" % (idempotency_key,))
        copy = HttpClient(self.base_url, self.secret_key, self.workspace_key, None, self.timeout, idempotency_key)
        copy._state = self._state
        return copy

    def withIdempotencyKey(self, idempotency_key):
        return self.with_idempotency_key(idempotency_key)

    def url(self, relative_url, query_params=None, **path_params):
        if query_params is None:
            query_params = {}
        return ApiResource(self, relative_url, query_params, **path_params)

    def execute(self, http_method, url, route_template, body_object=None):
        """
        Sends one request, and retries it as long as that's safe: on a 429, on a 409 IDEMPOTENCY_KEY_IN_USE, when a
        write never reached the server, and when the response of a write was lost on a route that honors
        idempotency keys. Every retry sends the same request, with the same Idempotency-Key.
        """
        write = None if http_method in SAFE_METHODS \
            else _Write(self._state, http_method + " " + route_template, self.idempotency_key or str(uuid.uuid4()))
        request = _Request(http_method, url, write.idempotency_key if write else None)
        headers = self.__headers(request)
        try:
            data = None if write is None else jsonpickle.encode(body_object, unpicklable=False)
        except Exception as cause:
            raise write.connection_failure(request, cause, Delivery.NOT_RETRYABLE) from cause

        retry_count = 0
        while True:
            try:
                response = requests.request(http_method, url, auth=(self.secret_key, ''), headers=headers, data=data,
                                            timeout=self.timeout)
            except Exception as cause:
                delivery = Delivery.of(cause)
                if write is None:
                    raise SeatsioException.from_connection_failure(
                        request, cause, outcome_is_unknown=delivery != Delivery.NEVER_SENT,
                        safe_to_retry_with_same_key=False) from cause
                if write.failed(delivery) and self.__wait_before_retry(retry_count, write):
                    retry_count += 1
                    continue
                raise write.connection_failure(request, cause, delivery) from cause
            if write is not None:
                write.answered(response)
            if is_retryable(response) and self.__wait_before_retry(retry_count, write):
                retry_count += 1
                continue
            if response.status_code >= 400:
                raise SeatsioException.from_response(request, response,
                                                     route_honors_keys=write is not None and write.route_honors_keys())
            return response

    def __headers(self, request):
        headers = {
            'X-Workspace-Key': str(self.workspace_key) if self.workspace_key else None,
            'X-Client-Lib': 'python'
        }
        if request.idempotency_key:
            headers[IDEMPOTENCY_KEY_HEADER] = request.idempotency_key
        return headers

    def __wait_before_retry(self, retry_count, write):
        # max_retries is the hard limit, whatever the reason for the retry. The retry window can only refuse more.
        if retry_count >= self._state.max_retries:
            return False
        delay = (2 ** (retry_count + 2)) / 10.0
        if write is not None and not write.may_retry_after(delay):
            return False
        # A KeyboardInterrupt (or any other exception) raised while sleeping ends the call: no further attempt
        self._state.clock.sleep(delay)
        return True


class ApiResource:
    def __init__(self, http_client, relative_url, query_params, **path_params):
        self.http_client = http_client
        self.relative_url = relative_url
        self.url = self.__create_full_url(http_client.base_url, relative_url, query_params, **path_params)

    @staticmethod
    def __create_full_url(base_url, relative_url, query_params, **path_params):
        for key in path_params:
            path_params[key] = quote(str(path_params[key]), safe='')
        full_url = base_url + relative_url.format(**path_params)
        if query_params:
            full_url += "?" + urlencode(query_params, True)
        return full_url

    def get(self):
        return self.__execute("GET").json()

    def get_raw(self):
        return self.__execute("GET").content

    def get_as(self, cls):
        return cls(self.get())

    def post(self, body=None):
        return self.__execute("POST", body)

    def post_empty_and_return(self, cls):
        return cls(self.post().json())

    def delete(self, body=None):
        return self.__execute("DELETE", body)

    def put(self, body=None):
        return self.__execute("PUT", body)

    def __execute(self, http_method, body=None):
        return self.http_client.execute(http_method, self.url, self.relative_url, body)


class _Request:
    """
    What a SeatsioException tells about the request that failed.
    """

    def __init__(self, http_method, url, idempotency_key):
        self.http_method = http_method
        self.url = url
        self.idempotency_key = idempotency_key


def is_retryable(response):
    return response.status_code == 429 or is_idempotency_key_in_use(response)


class Delivery(Enum):
    """
    How far a request that got no response went.
    """

    # Connection refused, connect timeout, DNS failure, TLS handshake failure: no byte of the request was sent.
    NEVER_SENT = 1
    # The request may have reached the server and run: read timeout, connection reset or closed, truncated response.
    RESPONSE_LOST = 2
    # Not a network failure (an invalid URL, a body that can't be encoded). Retrying gives the same result.
    NOT_RETRYABLE = 3

    @staticmethod
    def of(cause):
        if isinstance(cause, requests.exceptions.ConnectTimeout):
            return Delivery.NEVER_SENT
        if isinstance(cause, requests.exceptions.SSLError):
            return Delivery.NEVER_SENT if _failed_during_tls_handshake(cause) else Delivery.RESPONSE_LOST
        if isinstance(cause, requests.exceptions.ConnectionError):
            # Connection refused and DNS failures (urllib3's NameResolutionError is a NewConnectionError)
            return Delivery.NEVER_SENT if _caused_by(cause, NewConnectionError) else Delivery.RESPONSE_LOST
        if isinstance(cause, (requests.exceptions.Timeout, requests.exceptions.ChunkedEncodingError,
                              requests.exceptions.ContentDecodingError)):
            return Delivery.RESPONSE_LOST
        return Delivery.NOT_RETRYABLE


def _causes(error):
    """
    The error and everything it wraps: requests puts urllib3's MaxRetryError in args[0], which keeps the actual
    error in .reason; Python's own chaining is in __cause__ and __context__.
    """
    seen = []
    pending = [error]
    while pending:
        current = pending.pop()
        if current is None or not isinstance(current, BaseException) or any(current is s for s in seen):
            continue
        seen.append(current)
        pending.append(getattr(current, "reason", None))
        pending.extend(arg for arg in current.args if isinstance(arg, BaseException))
        pending.append(current.__cause__)
        pending.append(current.__context__)
    return seen


def _caused_by(error, error_type):
    return any(isinstance(e, error_type) for e in _causes(error))


def _failed_during_tls_handshake(error):
    """
    An SSL error can also happen while reading the response, after the request was sent. Only an error raised by
    the handshake proves that nothing was sent.
    """
    for e in _causes(error):
        traceback = e.__traceback__
        while traceback is not None:
            if traceback.tb_frame.f_code.co_name == "do_handshake":
                return True
            traceback = traceback.tb_next
    return False


class _Write:
    """
    The attempts of one POST, PUT or DELETE request, all sent with the same Idempotency-Key.
    """

    def __init__(self, state, route, idempotency_key):
        self.state = state
        self.route = route
        self.idempotency_key = idempotency_key
        self.start = state.clock.now()
        # Any response came back, or a response was lost: from then on, retries must start within the retry window
        self.may_have_reached_the_server = False
        # A response was lost, or the key was in use: a later failure that never reached the server has an
        # unknown outcome all the same
        self.may_have_run = False

    def answered(self, response):
        self.may_have_reached_the_server = True
        if is_idempotency_key_in_use(response):
            self.may_have_run = True
        self.state.remember(self.route, IdempotencyKeyStatus.of(response))

    def failed(self, delivery):
        """
        Records a connection failure. Returns whether it may be retried, retries left and time permitting.
        """
        if delivery == Delivery.NEVER_SENT:
            return True
        self.may_have_reached_the_server = True
        self.may_have_run = True
        return delivery == Delivery.RESPONSE_LOST and self.route_honors_keys()

    def may_retry_after(self, delay):
        return not self.may_have_reached_the_server or self.__starts_within_retry_window(delay)

    def __starts_within_retry_window(self, delay):
        return self.state.clock.now() + delay - self.start <= RETRY_WINDOW_SECONDS

    def route_honors_keys(self):
        return self.state.honors_keys(self.route)

    def connection_failure(self, request, cause, delivery):
        if delivery == Delivery.NOT_RETRYABLE:
            self.may_have_run = True
        safe_to_retry_with_same_key = not self.may_have_run \
            or (self.route_honors_keys() and self.__starts_within_retry_window(0))
        return SeatsioException.from_connection_failure(request, cause, self.may_have_run, safe_to_retry_with_same_key)


class _SharedState:
    """
    Shared by an HttpClient and the copies made with with_idempotency_key(): they use the same secret key, so the
    same company, and the server honors keys for the same routes.
    """

    def __init__(self, max_retries, clock):
        self.max_retries = max_retries
        self.clock = clock
        self._lock = threading.Lock()
        # Per "METHOD path template": whether the last response with a known Idempotency-Key-Status said the route
        # honors idempotency keys. No entry means unknown.
        self._routes_honoring_keys = {}

    def remember(self, route, status):
        if status is not None:
            with self._lock:
                self._routes_honoring_keys[route] = status.key_honored

    def honors_keys(self, route):
        with self._lock:
            return self._routes_honoring_keys.get(route) is True
