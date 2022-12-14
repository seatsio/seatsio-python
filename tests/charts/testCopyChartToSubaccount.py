from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartToSubaccountTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("my chart", "BOOTHS")
        subaccount = self.client.subaccounts.create()

        copied_chart = self.client.charts.copy_to_subaccount(chart.key, subaccount.id)

        subaccount_client = self.create_client(subaccount.secret_key, None)
        assert_that(copied_chart.name).is_equal_to("my chart")
        retrieved_chart = subaccount_client.charts.retrieve(copied_chart.key)
        assert_that(retrieved_chart.name).is_equal_to("my chart")
