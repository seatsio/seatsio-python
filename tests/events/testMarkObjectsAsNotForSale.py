from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MarkObjectsAsNotForSaleTest(SeatsioClientTest):

    def test_objects_and_categories(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_not_for_sale(event.key, ["o1", "o2"], ["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.for_sale_config.categories).contains_exactly("cat1", "cat2")

    def test_objects(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_not_for_sale(event.key, objects=["o1", "o2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.for_sale_config.categories).is_empty()

    def test_categories(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_not_for_sale(event.key, categories=["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).is_empty()
        assert_that(retrieved_event.for_sale_config.categories).contains_exactly("cat1", "cat2")
