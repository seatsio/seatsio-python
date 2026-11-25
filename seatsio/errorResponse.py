class ErrorResponse:
    """
    The JSON error body of a failed request: {"errors": [{"code": ..., "message": ...}], "requestId": ...}.
    """

    def __init__(self, errors, request_id):
        self.errors = errors
        self.request_id = request_id

    @staticmethod
    def parse_if_any(response):
        """
        None when the body is not a JSON object. Never raises: a missing or malformed "errors" list gives [].
        """
        if "application/json" not in (response.headers.get("content-type") or ""):
            return None
        try:
            body = response.json()
        except ValueError:
            return None
        if not isinstance(body, dict):
            return None
        errors = body.get("errors")
        errors = [error for error in errors if isinstance(error, dict)] if isinstance(errors, list) else []
        request_id = body.get("requestId")
        return ErrorResponse(errors, request_id if isinstance(request_id, str) else None)

    def first_error_code(self):
        return self.errors[0].get("code") if self.errors else None

    def has_error_code(self, code):
        return any(error.get("code") == code for error in self.errors)

    def messages(self):
        return [error["message"] for error in self.errors if isinstance(error.get("message"), str)]


def is_idempotency_key_in_use(response):
    if response.status_code != 409:
        return False
    error_response = ErrorResponse.parse_if_any(response)
    return error_response is not None and error_response.first_error_code() == "IDEMPOTENCY_KEY_IN_USE"
