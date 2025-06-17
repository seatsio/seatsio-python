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
            assert_that(e.errors[0]['code']).contains("WORKSPACE_NOT_FOUND")
