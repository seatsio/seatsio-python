from seatsio.errorResponse import ErrorResponse, is_idempotency_key_in_use
from seatsio.idempotencyKeyStatus import IdempotencyKeyStatus


class SeatsioException(Exception):
    """
    A failed request.

    For a POST or DELETE, ``idempotency_key`` is the Idempotency-Key the request carried, ``idempotency_key_honored``
    and ``replayed`` say what the server did with it (from the Idempotency-Key-Status response header), and
    ``outcome_is_unknown()`` and ``is_safe_to_retry_with_same_key()`` say whether and how the request can be retried.
    """

    def __init__(self, request, response=None, cause=None, route_honors_keys=False,
                 earlier_attempt_may_have_run=False, retry_window_open=True):
        self.cause = cause
        self.errors = None
        self.requestId = None
        self.idempotency_key = None
        # Whether the server honored the idempotency key of this request, according to the Idempotency-Key-Status
        # header of the response: True or False, or None when there was no response or the response didn't say.
        self.idempotency_key_honored = None
        # True if the server didn't execute the request again but replayed the recorded response of an earlier
        # request with the same idempotency key.
        self.replayed = False
        self._outcome_is_unknown = False
        self._safe_to_retry_with_same_key = False

        if isinstance(request, str):
            self.message = request
        else:
            self.idempotency_key = getattr(request, 'idempotency_key', None)
            self.message = self.__generic_message(request)
            if response is None:
                self._outcome_is_unknown = True
            else:
                self.__describe_response(response, route_honors_keys, earlier_attempt_may_have_run, retry_window_open)
        self.idempotencyKey = self.idempotency_key
        super(SeatsioException, self).__init__(self.message)

    def __describe_response(self, response, route_honors_keys, earlier_attempt_may_have_run, retry_window_open):
        error_response = ErrorResponse.parse_if_any(response)
        if error_response is not None:
            self.errors = error_response.errors
            self.requestId = error_response.request_id
            messages = error_response.messages()
            if messages:
                self.message = ", ".join(messages) + "."
        status = IdempotencyKeyStatus.of(response)
        self.idempotency_key_honored = None if status is None else status.key_honored
        self.replayed = status is IdempotencyKeyStatus.REPLAYED
        self._outcome_is_unknown = response.status_code >= 500 or is_idempotency_key_in_use(response) \
            or earlier_attempt_may_have_run
        key_honored = route_honors_keys if status is None else status.key_honored
        self._safe_to_retry_with_same_key = self._outcome_is_unknown \
            and self.idempotency_key is not None \
            and key_honored \
            and retry_window_open \
            and not self.replayed

    @staticmethod
    def __generic_message(request):
        http_method = getattr(request, 'http_method', '')
        url = getattr(request, 'url', '')
        return f"Error while executing {http_method} {url}".strip()

    @staticmethod
    def from_response(request, response, route_honors_keys=False, earlier_attempt_may_have_run=False,
                      retry_window_open=True):
        """
        :param route_honors_keys: whether the last response of the same route said the server honors idempotency
            keys for it. Used when this response doesn't say, e.g. a 502 from a proxy.
        :param earlier_attempt_may_have_run: an earlier attempt with the same key lost its response or found the key
            in use, so the outcome stays unknown whatever this response says
        :param retry_window_open: False once the key may have expired on the server
        """
        if response.status_code == 429:
            return RateLimitExceededException(request, response, route_honors_keys=route_honors_keys,
                                              earlier_attempt_may_have_run=earlier_attempt_may_have_run,
                                              retry_window_open=retry_window_open)
        elif SeatsioException.__is_best_available_objects_not_found(response):
            return BestAvailableObjectsNotFoundException(request, response, route_honors_keys=route_honors_keys,
                                                         earlier_attempt_may_have_run=earlier_attempt_may_have_run,
                                                         retry_window_open=retry_window_open)
        else:
            return SeatsioException(request, response, route_honors_keys=route_honors_keys,
                                    earlier_attempt_may_have_run=earlier_attempt_may_have_run,
                                    retry_window_open=retry_window_open)

    @staticmethod
    def from_connection_failure(request, cause, outcome_is_unknown, safe_to_retry_with_same_key):
        """
        A request that got no response.

        :param outcome_is_unknown: False if the request never reached the server
        :param safe_to_retry_with_same_key: True if a retry with the same idempotency key can't execute the request twice
        """
        exception = SeatsioException(request, cause=cause)
        exception._outcome_is_unknown = outcome_is_unknown
        exception._safe_to_retry_with_same_key = safe_to_retry_with_same_key and exception.idempotency_key is not None
        return exception

    def outcome_is_unknown(self):
        """
        True if the request may or may not have been executed: the response was lost after the request was sent, the
        server answered with a 5xx, or the key was still in use after all retries (the first request may still
        succeed). False for a request that never reached the server, and for every 4xx other than
        IDEMPOTENCY_KEY_IN_USE.
        """
        return self._outcome_is_unknown

    def is_safe_to_retry_with_same_key(self):
        """
        True if the same call, made again with this exception's idempotency_key (see Client.with_idempotency_key()),
        can't execute the request twice and may give a different result. That holds when the request never reached
        the server, or when its outcome is unknown and the server honors idempotency keys for it: known from the
        response or, when the response was lost, from the last response of the same route. Retry promptly: the
        server keeps a key for 10 minutes.
        """
        return self._safe_to_retry_with_same_key

    @staticmethod
    def __is_best_available_objects_not_found(response):
        error_response = ErrorResponse.parse_if_any(response)
        return error_response is not None and error_response.has_error_code('BEST_AVAILABLE_OBJECTS_NOT_FOUND')


class RateLimitExceededException(SeatsioException):

    def __init__(self, request, response=None, cause=None, route_honors_keys=False,
                 earlier_attempt_may_have_run=False, retry_window_open=True):
        super(RateLimitExceededException, self).__init__(request, response, cause, route_honors_keys,
                                  earlier_attempt_may_have_run, retry_window_open)


class BestAvailableObjectsNotFoundException(SeatsioException):

    def __init__(self, request, response=None, cause=None, route_honors_keys=False,
                 earlier_attempt_may_have_run=False, retry_window_open=True):
        super(BestAvailableObjectsNotFoundException, self).__init__(request, response, cause, route_honors_keys,
                                  earlier_attempt_may_have_run, retry_window_open)
