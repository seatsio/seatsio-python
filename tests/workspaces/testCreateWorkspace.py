from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateWorkspaceTest(SeatsioClientTest):

    def test_create_workspace(self):
        workspace = self.client.workspaces.create("my workspace")

        assert_that(workspace.id).is_not_zero()
        assert_that(workspace.name).is_equal_to("my workspace")
        assert_that(workspace.key).is_not_none()
        assert_that(workspace.secret_key).is_not_none()
        assert_that(workspace.is_test).is_false()
        assert_that(workspace.is_active).is_true()

    def test_create_test_workspace(self):
        workspace = self.client.workspaces.create("my workspace", True)

        assert_that(workspace.id).is_not_zero()
        assert_that(workspace.name).is_equal_to("my workspace")
        assert_that(workspace.key).is_not_none()
        assert_that(workspace.secret_key).is_not_none()
        assert_that(workspace.is_test).is_true()
        assert_that(workspace.is_active).is_true()
