class SeatsioException(Exception):

    def __init__(self, request, response):
        super(SeatsioException, self).__init__("Error while executing " + request.httpMethod + " " + request.url)
        if ("application/json" in response.headers["Content-Type"]):
            self.messages = response.body["messages"]
            self.requestId = response.body["requestId"]