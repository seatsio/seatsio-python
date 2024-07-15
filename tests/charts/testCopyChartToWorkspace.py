from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartToWorkspaceTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("my chart", "SIMPLE")
        workspace = self.client.workspaces.create("my ws")

        copied_chart = self.client.charts.copy_to_workspace(chart.key, workspace.key)

        workspace_client = self.create_client(workspace.secret_key, None)
        assert_that(copied_chart.name).is_equal_to("my chart")
        retrieved_chart = workspace_client.charts.retrieve(copied_chart.key)
        assert_that(retrieved_chart.name).is_equal_to("my chart")
        drawing = workspace_client.charts.retrieve_published_version(copied_chart.key)
        assert_that(drawing.venueType).is_equal_to("SIMPLE")
