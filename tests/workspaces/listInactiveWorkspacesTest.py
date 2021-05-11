from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListActiveWorkspacesTest(SeatsioClientTest):

    def test(self):
        ws1 = self.client.workspaces.create("ws1")
        self.client.workspaces.deactivate(ws1.key)

        self.client.workspaces.create("ws2")

        ws3 = self.client.workspaces.create("ws3")
        self.client.workspaces.deactivate(ws3.key)

        workspaces = self.client.workspaces.inactive.list()

        assert_that(workspaces).extracting("name").contains_exactly("ws3", "ws1")

    def test_filter(self):
        self.client.workspaces.create("someWorkspace")

        ws1 = self.client.workspaces.create("anotherWorkspace")
        self.client.workspaces.deactivate(ws1.key)

        ws2 = self.client.workspaces.create("anotherAnotherWorkspace")
        self.client.workspaces.deactivate(ws2.key)

        self.client.workspaces.create("anotherAnotherAnotherWorkspace")

        workspaces = self.client.workspaces.inactive.list("another")

        assert_that(workspaces).extracting("name").contains_exactly("anotherAnotherWorkspace", "anotherWorkspace")
