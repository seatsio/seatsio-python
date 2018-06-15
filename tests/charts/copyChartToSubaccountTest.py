import seatsio
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CopyChartToSubaccountTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create("my chart", "BOOTHS")
        subaccount = self.client.subaccounts.create()

        copied_chart = self.client.charts.copy_to_subaccount(chart.key, subaccount.id)

        subaccount_client = seatsio.Client(subaccount.secret_key, "https://api-staging.seatsio.net")
        assert_that(copied_chart.name).is_equal_to("my chart")
        retrieved_chart = subaccount_client.charts.retrieve(copied_chart.key)
        assert_that(retrieved_chart.name).is_equal_to("my chart")
        drawing = subaccount_client.charts.retrieve_published_version(copied_chart.key)
        assert_that(drawing.venueType).is_equal_to("BOOTHS")
