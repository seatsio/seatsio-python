from seatsio import ForSaleConfig
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EditForSaleConfigForEventsTest(SeatsioClientTest):

    def test_mark_objects_for_sale(self):
        chart_key = self.create_test_chart()
        for_sale_config = ForSaleConfig.create_new(False, ["A-1", "A-2", "A-3"])
        event1 = self.client.events.create(chart_key, for_sale_config=for_sale_config)
        event2 = self.client.events.create(chart_key, for_sale_config=for_sale_config)
        request = {
            event1.key: {"for_sale": [{"object": "A-1"}]},
            event2.key: {"for_sale": [{"object": "A-2"}]}
        }

        self.client.events.edit_for_sale_config_for_events(request)

        retrieved_event1 = self.client.events.retrieve(event1.key)
        assert_that(retrieved_event1.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event1.for_sale_config.objects).contains_exactly("A-2", "A-3")

        retrieved_event2 = self.client.events.retrieve(event2.key)
        assert_that(retrieved_event2.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event2.for_sale_config.objects).contains_exactly("A-1", "A-3")

    def test_mark_objects_not_for_sale(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)
        request = {
            event1.key: {"not_for_sale": [{"object": "A-1"}]},
            event2.key: {"not_for_sale": [{"object": "A-2"}]}
        }

        self.client.events.edit_for_sale_config_for_events(request)

        retrieved_event1 = self.client.events.retrieve(event1.key)
        assert_that(retrieved_event1.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event1.for_sale_config.objects).contains_exactly("A-1")

        retrieved_event2 = self.client.events.retrieve(event2.key)
        assert_that(retrieved_event2.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event2.for_sale_config.objects).contains_exactly("A-2")