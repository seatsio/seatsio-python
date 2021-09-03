import seatsio
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class WorkspaceKeyAuthenticationTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()

        subaccount_client = self.create_client(self.user["secretKey"], subaccount.public_key)
        hold_token = subaccount_client.hold_tokens.create()

        assert_that(hold_token.workspace_key).is_equal_to(subaccount.public_key)
