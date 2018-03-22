from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListFirstPageOfChartsTest(SeatsioClientTest):

    def test_allOnFirstPage(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list_first_page()

        assert_that(charts.items).extracting("id").contains_exactly(chart3.id, chart2.id, chart1.id)
        assert_that(charts.next_page_starts_after).is_none()
        assert_that(charts.previous_page_ends_before).is_none()

    def test_someOnFirstPage(self):
        chart1 = self.client.charts.create()
        chart2 = self.client.charts.create()
        chart3 = self.client.charts.create()

        charts = self.client.charts.list_first_page(page_size=2)

        assert_that(charts.items).extracting("id").contains_exactly(chart3.id, chart2.id)
        assert_that(charts.next_page_starts_after).is_equal_to(chart2.id)
        assert_that(charts.previous_page_ends_before).is_none()
