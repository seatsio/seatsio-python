class SeatsioException(Exception):
    def __init__(self, message, requestId):
        super(SeatsioException, self).__init__(message)
        self.requestId = requestId

