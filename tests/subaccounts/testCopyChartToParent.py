from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartToParentTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create()
        chart = self.newClient(subaccount.secret_key).charts.create("aChart")

        copied_chart = self.client.subaccounts.copy_chart_to_parent(subaccount.id, chart.key)

        assert_that(copied_chart.name).is_equal_to("aChart")

        retrieved_chart = self.client.charts.retrieve(copied_chart.key)
        assert_that(retrieved_chart.name).is_equal_to("aChart")
