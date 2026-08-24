
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RemoveWorkspaceSecretKeyTest(SeatsioClientTest):

    def test(self):
        workspace = self.client.workspaces.create("a ws")
        new_secret_key = self.client.workspaces.add_secret_key(workspace.key)

        retrieved_workspace = self.client.workspaces.retrieve(workspace.key)
        assert_that(retrieved_workspace.secret_keys).contains_exactly_in_any_order(workspace.secret_key, new_secret_key)

        self.client.workspaces.remove_secret_key(workspace.key, workspace.secret_key)

        final_state_workspace = self.client.workspaces.retrieve(workspace.key)
        assert_that(final_state_workspace.secret_keys).contains_exactly(new_secret_key)
