from datetime import datetime

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateEventTest(SeatsioClientTest):

    def test_updateChartKey(self):
        chart1 = self.client.charts.create()
        event = self.client.events.create(chart1.key)
        chart2 = self.client.charts.create()

        self.client.events.update(event.key, chart_key=chart2.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.key).is_equal_to(event.key)
        assert_that(retrieved_event.chart_key).is_equal_to(chart2.key)
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateEventKey(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.update(event.key, event_key="newKey")

        retrieved_event = self.client.events.retrieve("newKey")
        assert_that(retrieved_event.key).is_equal_to("newKey")
        assert_that(retrieved_event.id).is_equal_to(event.id)
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateBookWholeTables(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.update(event.key, book_whole_tables=True)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.book_whole_tables).is_true()
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

        self.client.events.update(event.key, book_whole_tables=False)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.book_whole_tables).is_false()
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateTableBookingModes(self):
        chart_key = self.create_test_chart_with_tables()
        event = self.client.events.create(chart_key, table_booking_modes={"T1": "BY_TABLE"})

        self.client.events.update(event.key, table_booking_modes={"T1": "BY_SEAT"})

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.table_booking_modes).is_equal_to({"T1": "BY_SEAT"})
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)
