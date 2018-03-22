from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListChartsBeforeTest(SeatsioClientTest):

    def test_withPreviousPage(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list_page_before(chart1.id)

        assert_that(charts.items).extracting("id").contains_exactly(chart3.id, chart2.id)
        assert_that(charts.next_page_starts_after).is_equal_to(chart2.id)
        assert_that(charts.previous_page_ends_before).is_none()

    def test_withNextAndPreviousPages(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list_page_before(chart1.id, page_size=1)

        assert_that(charts.items).extracting("id").contains_exactly(chart2.id)
        assert_that(charts.next_page_starts_after).is_equal_to(chart2.id)
        assert_that(charts.previous_page_ends_before).is_equal_to(chart2.id)
