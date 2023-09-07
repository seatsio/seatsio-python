import seatsio
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class WorkspaceKeyAuthenticationTest(SeatsioClientTest):

    def test(self):
        workspace = self.client.workspaces.create('some workspace')

        workspace_client = self.create_client(self.user["secretKey"], workspace.key)
        hold_token = workspace_client.hold_tokens.create()

        assert_that(hold_token.workspace_key).is_equal_to(workspace.key)
