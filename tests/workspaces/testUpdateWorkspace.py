from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateWorkspaceTest(SeatsioClientTest):

    def test(self):
        workspace = self.client.workspaces.create("my workspace")

        self.client.workspaces.update(workspace.key, "my ws")

        retrieved_workspace = self.client.workspaces.retrieve(workspace.key)
        assert_that(retrieved_workspace.id).is_not_zero()
        assert_that(retrieved_workspace.name).is_equal_to("my ws")
        assert_that(retrieved_workspace.key).is_not_none()
        assert_that(retrieved_workspace.secret_key).is_not_none()
        assert_that(retrieved_workspace.is_test).is_false()
