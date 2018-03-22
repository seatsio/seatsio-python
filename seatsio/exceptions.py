class SeatsioException(Exception):

    def __init__(self, request, response=None, cause=None):
        if (response is not None) and ("application/json" in response.headers["Content-Type"]):
            body = response.json()
            self.messages = body["messages"]
            self.requestId = body["requestId"]
            self.cause = cause
            self.message = self.__build_exception_message(request, response)
            super(SeatsioException, self).__init__(self.message)
        else:
            self.messages = None
            self.requestId = None
            self.cause = cause
            self.message = "Error while executing " + request.httpMethod + " " + request.url + ". Cause: " + str(cause.args)
            super(SeatsioException, self).__init__(self.message)

    def __build_exception_message(self, request, response):
        exception_message = request.httpMethod + " " + request.url + " resulted in a "
        exception_message += str(response.status_code) + " " + str(response.reason) + " response."
        exception_message += " Reason: " + ", ".join(self.messages) + "."
        exception_message += " Request ID: " + self.requestId
        return exception_message
