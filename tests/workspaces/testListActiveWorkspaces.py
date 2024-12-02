from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListActiveWorkspacesTest(SeatsioClientTest):

    def test(self):
        self.client.workspaces.create("ws1")

        ws2 = self.client.workspaces.create("ws2")
        self.client.workspaces.deactivate(ws2.key)

        self.client.workspaces.create("ws3")

        workspaces = self.client.workspaces.active.list()

        assert_that(workspaces).extracting("name").contains_exactly("ws3", "ws1", "Production workspace")

    def test_filter(self):
        self.client.workspaces.create("someWorkspace")
        self.client.workspaces.create("anotherWorkspace")
        self.client.workspaces.create("anotherAnotherWorkspace")

        ws = self.client.workspaces.create("anotherAnotherAnotherWorkspace")
        self.client.workspaces.deactivate(ws.key)

        workspaces = self.client.workspaces.active.list("another")

        assert_that(workspaces).extracting("name").contains_exactly("anotherAnotherWorkspace", "anotherWorkspace")
