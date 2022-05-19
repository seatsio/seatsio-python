from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListFirstPageOfEventsTest(SeatsioClientTest):

    def test_allOnFirstPage(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.events.list_first_page()

        assert_that(events.items).extracting("id").contains_exactly(event3.id, event2.id, event1.id)
        assert_that(events.next_page_starts_after).is_none()
        assert_that(events.previous_page_ends_before).is_none()

    def test_someOnFirstPage(self):
        chart = self.client.charts.create()
        event1 = self.client.events.create(chart.key)
        event2 = self.client.events.create(chart.key)
        event3 = self.client.events.create(chart.key)

        events = self.client.events.list_first_page(page_size=2)

        assert_that(events.items).extracting("id").contains_exactly(event3.id, event2.id)
        assert_that(events.next_page_starts_after).is_equal_to(event2.id)
        assert_that(events.previous_page_ends_before).is_none()
