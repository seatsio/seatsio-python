from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class DeactivateWorkspaceTest(SeatsioClientTest):

    def test_delete_inactive_workspace(self):
        workspace = self.client.workspaces.create("a ws")
        self.client.workspaces.deactivate(workspace.key)

        self.client.workspaces.delete(workspace.key)

        try:
            self.client.workspaces.retrieve(workspace.key)
            self.fail("expected an exception")
        except SeatsioException as e:
            assert_that(e.message).contains("No workspace found with public key '" + workspace.key + "'")

    def test_delete_active_workspace(self):
        workspace = self.client.workspaces.create("a ws")

        try:
            self.client.workspaces.delete(workspace.key)
            self.fail("expected an exception")
        except SeatsioException as e:
            assert_that(e.message).contains("Cannot delete active workspace, please deactivate it first")
