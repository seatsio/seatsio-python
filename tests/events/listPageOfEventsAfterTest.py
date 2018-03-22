from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListEventsAfterTest(SeatsioClientTest):

    def test_withPreviousPage(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.events.list_page_after(event3.id)

        assert_that(events.items).extracting("id").contains_exactly(event2.id, event1.id)
        assert_that(events.next_page_starts_after).is_none()
        assert_that(events.previous_page_ends_before).is_equal_to(event2.id)

    def test_withNextAndPreviousPages(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.events.list_page_after(event3.id, page_size=1)

        assert_that(events.items).extracting("id").contains_exactly(event2.id)
        assert_that(events.next_page_starts_after).is_equal_to(event2.id)
        assert_that(events.previous_page_ends_before).is_equal_to(event2.id)
