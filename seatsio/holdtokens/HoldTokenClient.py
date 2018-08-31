from seatsio.domain import HoldToken


class HoldTokensClient:

    def __init__(self, http_client):
        self.http_client = http_client

    def create(self, expires_in_minutes=None):
        body = {}
        if expires_in_minutes:
            body["expiresInMinutes"] = expires_in_minutes
        response = self.http_client.url("/hold-tokens").post(body)
        return HoldToken(response.json())

    def retrieve(self, hold_token):
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).get()
        return HoldToken(response)

    def expire_in_minutes(self, hold_token, expires_in_minutes):
        body = {"expiresInMinutes": expires_in_minutes}
        response = self.http_client.url("/hold-tokens/{holdToken}", holdToken=hold_token).post(body)
        return HoldToken(response.json())
