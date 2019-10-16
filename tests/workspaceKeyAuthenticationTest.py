import seatsio
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class WorkspaceKeyAuthenticationTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()

        subaccount_client = seatsio.Client(self.user["secretKey"], subaccount.workspace.key, "https://api-staging.seatsio.net")
        hold_token = subaccount_client.hold_tokens.create()

        assert_that(hold_token.workspaceKey).is_equal_to(subaccount.workspace.key)
