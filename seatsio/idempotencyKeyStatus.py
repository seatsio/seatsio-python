from enum import Enum

IDEMPOTENCY_KEY_HEADER = "Idempotency-Key"
IDEMPOTENCY_KEY_STATUS_HEADER = "Idempotency-Key-Status"


class IdempotencyKeyStatus(Enum):
    """
    The value of the Idempotency-Key-Status response header: what the server did with the Idempotency-Key of a
    POST or DELETE request that reached a route.
    """

    EXECUTED = ("executed", True)
    REPLAYED = ("replayed", True)
    IN_USE = ("in-use", True)
    REUSED = ("reused", True)
    IGNORED = ("ignored", False)

    def __init__(self, header_value, key_honored):
        self.header_value = header_value
        # True if the route honors idempotency keys, so a retry with the same key can't execute the request twice
        self.key_honored = key_honored

    @staticmethod
    def of(response):
        """
        The status in the response, or None when the header is absent or has a value this client doesn't know.
        Unknown values count as absent, so that a future value or a proxy that strips the header errs towards
        not retrying.
        """
        value = (response.headers.get(IDEMPOTENCY_KEY_STATUS_HEADER) or "").strip().lower()
        for status in IdempotencyKeyStatus:
            if status.header_value == value:
                return status
        return None
