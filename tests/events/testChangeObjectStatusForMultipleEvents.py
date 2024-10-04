from seatsio.domain import EventObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeBestAvailableObjectStatusTest(SeatsioClientTest):

    def test_customStatus(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.change_object_status(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
            status="stat"
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to("stat")
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to("stat")
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to("stat")
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to("stat")

    def test_book(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.book(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(EventObjectInfo.BOOKED)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(EventObjectInfo.BOOKED)

    def test_put_up_for_resale(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.put_up_for_resale(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(EventObjectInfo.RESALE)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(EventObjectInfo.RESALE)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(EventObjectInfo.RESALE)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(EventObjectInfo.RESALE)


    def test_hold(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
            hold_token=hold_token.hold_token
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(EventObjectInfo.HELD)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(EventObjectInfo.HELD)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(EventObjectInfo.HELD)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(EventObjectInfo.HELD)

    def test_release(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.book(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        self.client.events.release(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(EventObjectInfo.FREE)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(EventObjectInfo.FREE)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(EventObjectInfo.FREE)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(EventObjectInfo.FREE)

    def fetch_status(self, event, o):
        return self.client.events.retrieve_object_info(event, o).status
