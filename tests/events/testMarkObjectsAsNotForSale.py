from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MarkObjectsAsNotForSaleTest(SeatsioClientTest):

    def test_objects_and_categories(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.mark_as_not_for_sale(event.key, ["o1", "o2"], {"GA1": 3}, ["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.for_sale_config.area_places).is_equal_to({"GA1": 3})
        assert_that(retrieved_event.for_sale_config.categories).contains_exactly("cat1", "cat2")

    def test_objects(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_not_for_sale(event.key, objects=["o1", "o2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).contains_exactly("o1", "o2")
        assert_that(retrieved_event.for_sale_config.area_places).is_equal_to({})
        assert_that(retrieved_event.for_sale_config.categories).is_empty()

    def test_categories(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_as_not_for_sale(event.key, categories=["cat1", "cat2"])

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config.for_sale).is_false()
        assert_that(retrieved_event.for_sale_config.objects).is_empty()
        assert_that(retrieved_event.for_sale_config.area_places).is_equal_to({})
        assert_that(retrieved_event.for_sale_config.categories).contains_exactly("cat1", "cat2")

    def test_num_not_for_sale_is_correctly_exposed(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.mark_as_not_for_sale(event.key, [], {"GA1": 3}, [])

        info = self.client.events.retrieve_object_info(event.key, "GA1")
        assert_that(info.num_not_for_sale).is_equal_to(3)
