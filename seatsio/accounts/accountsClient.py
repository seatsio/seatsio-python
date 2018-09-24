from seatsio.domain import Account

class AccountsClient():

    def __init__(self, http_client):
        self.http_client = http_client

    def retrieve_my_account(self):
        response = self.http_client.url("/accounts/me").get()
        return Account(response)