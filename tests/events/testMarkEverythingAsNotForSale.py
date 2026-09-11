from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class MarkEverythingAsNotForSaleTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        event = self.client.events.create(chart.key)

        self.client.events.mark_everything_as_not_for_sale(event.key)

        retrieved_event = self.client.events.retrieve(event.key)
        assert_that(retrieved_event.for_sale_config).is_not_none()
        assert_that(retrieved_event.for_sale_config.for_sale).is_true()
        assert_that(retrieved_event.for_sale_config.objects).is_empty()
        assert_that(retrieved_event.for_sale_config.area_places).is_equal_to({})
        assert_that(retrieved_event.for_sale_config.categories).is_empty()



