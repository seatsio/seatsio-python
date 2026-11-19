from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListEventsOfChartTest(SeatsioClientTest):

    def test_all(self):
        chart = self.client.charts.create()
        other_chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        self.client.events.create(other_chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.charts.events(chart.key).list()

        assert_that(events).extracting("key").contains_exactly(event3.key, event2.key, event1.key)

    def test_pages(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        first_page = self.client.charts.events(chart.key).first_page(page_size=2)
        page_after = self.client.charts.events(chart.key).page_after(first_page.next_page_starts_after, page_size=2)

        assert_that(first_page.items).extracting("id").contains_exactly(event3.id, event2.id)
        assert_that(first_page.next_page_starts_after).is_equal_to(event2.id)
        assert_that(page_after.items).extracting("id").contains_exactly(event1.id)
        assert_that(page_after.next_page_starts_after).is_none()
