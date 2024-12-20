class SeatsioException(Exception):

    def __init__(self, request, response=None, cause=None):
        if (response is not None) and ("application/json" in response.headers.get("content-type", "")):
            body = response.json()
            self.errors = body["errors"]
            self.requestId = body["requestId"]
            self.cause = cause
            self.message = self.__build_exception_message()
            super(SeatsioException, self).__init__(self.message)
        else:
            self.errors = None
            self.requestId = None
            self.cause = cause
            self.message = "Error while executing " + request.http_method + " " + request.url
            super(SeatsioException, self).__init__(self.message)

    @staticmethod
    def from_response(request, response):
        if response.status_code == 429:
            return RateLimitExceededException(request, response)
        elif SeatsioException.__is_best_available_objects_not_found(response):
            return BestAvailableObjectsNotFoundException(request, response)
        else:
            return SeatsioException(request, response)

    @staticmethod
    def __is_best_available_objects_not_found(response):
        if "application/json" not in response.headers.get("content-type", ""):
            return False
        body = response.json()
        if "errors" not in body:
            return False
        for error in body["errors"]:
            if isinstance(error, dict) and 'code' in error:
                if error['code'] == 'BEST_AVAILABLE_OBJECTS_NOT_FOUND':
                    return True
        return False

    def __build_exception_message(self):
        return ", ".join(self.__map_errors_to_message(self.errors)) + "."

    def __map_errors_to_message(self, errors):
        return list(map(lambda e: e.get("message"), errors))


class RateLimitExceededException(SeatsioException):

    def __init__(self, request, response=None, cause=None):
        super(RateLimitExceededException, self).__init__(request, response, cause)

class BestAvailableObjectsNotFoundException(SeatsioException):

    def __init__(self, request, response=None, cause=None):
        super(BestAvailableObjectsNotFoundException, self).__init__(request, response, cause)
