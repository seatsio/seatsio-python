import seatsio
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class AccountIdAuthenticationTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()

        subaccount_client = seatsio.Client(self.user["secretKey"], subaccount.account_id, "https://api-staging.seatsio.net")
        hold_token = subaccount_client.hold_tokens.create()

        assert_that(hold_token.account_id).is_equal_to(subaccount.account_id)
