from seatsio.unirestUtil import Get


class SeatsioClient:

    def __init__(self, secretKey, baseUrl):
        self.secretKey = secretKey
        self.baseUrl = baseUrl

    def charts(self):
        return Charts(self.secretKey, self.baseUrl)


class Charts():

    def __init__(self, secretKey, baseUrl):
        self.secretKey = secretKey
        self.baseUrl = baseUrl

    def retrieve(self, chartKey):
        url = self.baseUrl + "/charts/" + chartKey
        response = Get(url).basicAuth(self.secretKey, '').execute()
        # TODO create chart object
        return response
