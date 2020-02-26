from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllWorkspacesTest(SeatsioClientTest):

    def test(self):
        self.client.workspaces.create("ws1")
        self.client.workspaces.create("ws2")
        self.client.workspaces.create("ws3")

        workspaces = self.client.workspaces.list()

        assert_that(workspaces).extracting("name").contains_exactly("ws3", "ws2", "ws1", "Main workspace")

    def test_filter(self):
        self.client.workspaces.create("someWorkspace")
        self.client.workspaces.create("anotherWorkspace")
        self.client.workspaces.create("anotherAnotherWorkspace")

        workspaces = self.client.workspaces.list("another")

        assert_that(workspaces).extracting("name").contains_exactly("anotherAnotherWorkspace", "anotherWorkspace")
