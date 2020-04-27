from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RegenerateWorkspaceSecretKeyTest(SeatsioClientTest):

    def test(self):
        workspace = self.client.workspaces.create("a ws")

        new_secret_key = self.client.workspaces.regenerate_secret_key(workspace.key)

        assert_that(new_secret_key).is_not_blank().is_not_equal_to(workspace.secret_key)
        retrieved_workspace = self.client.workspaces.retrieve(workspace.key)
        assert_that(retrieved_workspace.secret_key).is_equal_to(new_secret_key)
