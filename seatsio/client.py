from seatsio import unirestUtil


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
        response = unirestUtil.get(url, self.secretKey)
        return response
