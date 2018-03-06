class SeatsioException(Exception):
    httpCodes = {
        200: "OK",
        404: "Not Found"
    }

    def __init__(self, request, response=None):
        if response and ("application/json" in response.headers["Content-Type"]):
            self.messages = response.body["messages"]
            self.requestId = response.body["requestId"]
            super(SeatsioException, self).__init__(self.__buildExceptionMessage(request, response))
        else:
            self.messages = None
            self.requestId = None
            super(SeatsioException, self).__init__("Error while executing " + request.httpMethod + " " + request.url)

    def __buildExceptionMessage(self, request, response):
        exceptionMessage = request.httpMethod + " " + request.url + " resulted in a " + str(response.code) + " " + \
                           self.httpCodes[response.code] + " response."
        exceptionMessage += " Reason: " + ", ".join(self.messages) + "."
        exceptionMessage += " Request ID: " + self.requestId
        return exceptionMessage
