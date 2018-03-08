class SeatsioException(Exception):
    httpCodes = {
        200: "OK",
        400: "Bad Request",
        404: "Not Found"
    }

    def __init__(self, request, response=None, cause=None):
        if response and ("application/json" in response.headers["Content-Type"]):
            self.messages = response.body["messages"]
            self.requestId = response.body["requestId"]
            self.cause = cause
            super(SeatsioException, self).__init__(self.__build_exception_message(request, response))
        else:
            self.messages = None
            self.requestId = None
            self.cause = cause
            super(SeatsioException, self).__init__(
                "Error while executing " + request.httpMethod + " " + request.url + ". Cause: " + cause.message)

    def __build_exception_message(self, request, response):
        exception_message = request.httpMethod + " " + request.url + " resulted in a "
        exception_message += str(response.code) + " " + self.httpCodes[response.code] + " response."
        exception_message += " Reason: " + ", ".join(self.messages) + "."
        exception_message += " Request ID: " + self.requestId
        return exception_message
