from datetime import datetime, date

from seatsio import TableBookingConfig, Category
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateEventTest(SeatsioClientTest):

    def test_updateEventKey(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.update(event.key, event_key="newKey")

        retrieved_event = self.client.events.retrieve("newKey")
        assert_that(retrieved_event.key).is_equal_to("newKey")
        assert_that(retrieved_event.id).is_equal_to(event.id)
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateTableBookingModes(self):
        chart_key = self.create_test_chart_with_tables()
        event = self.client.events.create(chart_key, table_booking_config=TableBookingConfig.custom({"T1": "BY_TABLE"}))

        self.client.events.update(event.key, table_booking_config=TableBookingConfig.custom({"T1": "BY_SEAT"}))

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.table_booking_config).is_equal_to(TableBookingConfig.custom({"T1": "BY_SEAT"}))
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateObjectCategories(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, object_categories={'A-1': 10})

        self.client.events.update(event.key, object_categories={'A-2': 9})

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.object_categories).is_equal_to({'A-2' : 9})

    def test_removeObjectCategories(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key, object_categories={'A-1': 10})

        self.client.events.remove_object_categories(event.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.object_categories).is_none()

    def test_updateCategories(self):
        chart_key = self.create_test_chart()
        cat1 = Category(key='eventCategory1', label='Event Level Category 1', color='#AAABBB')
        cat2 = Category(key='eventCategory2', label='Event Level Category 2', color='#BBBCCC')
        event = self.client.events.create(chart_key, categories=[cat1])

        self.client.events.update(event.key, categories=[cat2])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.categories).extracting("key").contains("eventCategory2")

    def test_removeCategories(self):
        chart_key = self.create_test_chart()
        cat1 = Category(key='eventCategory1', label='Event Level Category 1', color='#AAABBB')
        event = self.client.events.create(chart_key, categories=[cat1])

        self.client.events.remove_categories(event.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.categories).extracting("key").does_not_contain("eventCategory1")

    def test_updateName(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key, name="An event")

        self.client.events.update(event.key, name="Another event")

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.name).is_equal_to("Another event")

    def test_updateDate(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key, date=date(2022, 1, 10))

        self.client.events.update(event.key, date=date(2023, 1, 10))

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.date).is_equal_to(date(2023, 1, 10))

    def test_updateIsInThePast(self):
        chart = self.client.charts.create()
        self.client.seasons.create(chart.key, event_keys=["event1"])

        self.client.events.update("event1", is_in_the_past=True)
        retrieved_event = self.client.events.retrieve("event1")
        assert_that(retrieved_event.is_in_the_past).is_true()
