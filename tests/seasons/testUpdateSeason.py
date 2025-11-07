from datetime import datetime, date

from seatsio import TableBookingConfig, Category
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateSeasonTest(SeatsioClientTest):

    def test_updateEventKey(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key)

        self.client.seasons.update(season.key, event_key="newKey")

        retrieved_season = self.client.seasons.retrieve("newKey")
        assert_that(retrieved_season.key).is_equal_to("newKey")
        assert_that(retrieved_season.id).is_equal_to(season.id)
        assert_that(retrieved_season.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateTableBookingModes(self):
        chart_key = self.create_test_chart_with_tables()
        season = self.client.seasons.create(chart_key, table_booking_config=TableBookingConfig.custom({"T1": "BY_TABLE"}))

        self.client.seasons.update(season.key, table_booking_config=TableBookingConfig.custom({"T1": "BY_SEAT"}))

        retrieved_season = self.client.seasons.retrieve(season.key)
        assert_that(retrieved_season.table_booking_config).is_equal_to(TableBookingConfig.custom({"T1": "BY_SEAT"}))
        assert_that(retrieved_season.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateObjectCategories(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key, object_categories={'A-1': 10})

        self.client.seasons.update(season.key, object_categories={'A-2': 9})

        retrieved_season = self.client.seasons.retrieve(season.key)
        assert_that(retrieved_season.object_categories).is_equal_to({'A-2' : 9})

    def test_updateCategories(self):
        chart_key = self.create_test_chart()
        cat1 = Category(key='eventCategory1', label='Event Level Category 1', color='#AAABBB')
        cat2 = Category(key='eventCategory2', label='Event Level Category 2', color='#BBBCCC')
        season = self.client.seasons.create(chart_key, categories=[cat1])

        self.client.seasons.update(season.key, categories=[cat2])

        retrieved_season = self.client.seasons.retrieve(season.key)
        assert_that(retrieved_season.categories).extracting("key").contains("eventCategory2")

    def test_updateName(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key, name="A season")

        self.client.seasons.update(season.key, name="Another season")

        retrieved_season = self.client.seasons.retrieve(season.key)
        assert_that(retrieved_season.name).is_equal_to("Another season")

    def test_update_for_sale_propagated(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key)

        self.client.seasons.update(season.key, for_sale_propagated=False)

        retrieved_season = self.client.seasons.retrieve(season.key)
        assert_that(retrieved_season.for_sale_propagated).is_false()
