from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class DeactivateWorkspaceTest(SeatsioClientTest):

    def test(self):
        workspace = self.client.workspaces.create("a ws")

        self.client.workspaces.deactivate(workspace.key)

        retrieved_workspace = self.client.workspaces.retrieve(workspace.key)
        assert_that(retrieved_workspace.is_active).is_false()
