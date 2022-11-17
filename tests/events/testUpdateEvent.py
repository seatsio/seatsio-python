from datetime import datetime

from seatsio import SocialDistancingRuleset, TableBookingConfig, Category
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

    def test_updateTableBookingModes(self):
        chart_key = self.create_test_chart_with_tables()
        event = self.client.events.create(chart_key, table_booking_config=TableBookingConfig.custom({"T1": "BY_TABLE"}))

        self.client.events.update(event.key, table_booking_config=TableBookingConfig.custom({"T1": "BY_SEAT"}))

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.table_booking_config).is_equal_to(TableBookingConfig.custom({"T1": "BY_SEAT"}))
        assert_that(retrieved_event.updated_on).is_between_now_minus_and_plus_minutes(datetime.utcnow(), 1)

    def test_updateSocialDistancingRulesetKey(self):
        chart_key = self.create_test_chart()
        self.client.charts.save_social_distancing_rulesets(chart_key, {
            'ruleset1': SocialDistancingRuleset(name='My first ruleset'),
            'ruleset2': SocialDistancingRuleset(name='My second ruleset'),
        })
        event = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset1')

        self.client.events.update(event.key, social_distancing_ruleset_key='ruleset2')

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.social_distancing_ruleset_key).is_equal_to('ruleset2')

    def test_removeSocialDistancingRulesetKey(self):
        chart_key = self.create_test_chart()
        self.client.charts.save_social_distancing_rulesets(chart_key, {
            'ruleset1': SocialDistancingRuleset(name='My first ruleset')
        })
        event = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset1')

        self.client.events.remove_social_distancing_ruleset_key(event.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.social_distancing_ruleset_key).is_none()

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

