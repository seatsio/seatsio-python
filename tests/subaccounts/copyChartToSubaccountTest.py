from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartToParentTest(SeatsioClientTest):

    def test(self):
        from_subaccount = self.client.subaccounts.create()
        chart = self.newClient(from_subaccount.secretKey).charts.create("aChart")
        to_subaccount = self.client.subaccounts.create()

        copied_chart = self.client.subaccounts.copy_chart_to_subaccount(from_subaccount.id, to_subaccount.id, chart.key)

        assert_that(copied_chart.name).is_equal_to("aChart")
        retrieved_chart = self.newClient(to_subaccount.secretKey).charts.retrieve(copied_chart.key)
        assert_that(retrieved_chart.name).is_equal_to("aChart")
