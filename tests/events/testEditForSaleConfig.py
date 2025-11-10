from seatsio import ForSaleConfig
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class EditForSaleConfigTest(SeatsioClientTest):

    def test_mark_objects_not_for_sale(self):
        chart_key = self.create_test_chart()
        for_sale_config = ForSaleConfig.create_new(False, ["A-1", "A-2", "A-3"])
        event = self.client.events.create(chart_key, for_sale_config=for_sale_config)

        result = self.client.events.edit_for_sale_config(event.key, [{"object": "A-1"}, {"object": "A-2"}])

        assert_that(result.for_sale_config.for_sale).is_false()
        assert_that(result.for_sale_config.objects).contains_exactly("A-3")

    def test_rate_limit_info_is_returned(self):
        chart_key = self.create_test_chart()
        for_sale_config = ForSaleConfig.create_new(False, ["A-1", "A-2", "A-3"])
        event = self.client.events.create(chart_key, for_sale_config=for_sale_config)

        result = self.client.events.edit_for_sale_config(event.key, [{"object": "A-1"}, {"object": "A-2"}])

        assert_that(result.rate_limit_info.rate_limit_remaining_calls).is_equal_to(9)
        assert_that(result.rate_limit_info.rate_limit_reset_date).is_not_none()

    def test_mark_objects_for_sale(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        result = self.client.events.edit_for_sale_config(event.key, None, [{"object": "A-1"}, {"object": "A-2"}])

        assert_that(result.for_sale_config.for_sale).is_false()
        assert_that(result.for_sale_config.objects).contains_exactly("A-1", "A-2")

    def test_mark_places_in_area_not_for_sale(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        result = self.client.events.edit_for_sale_config(event.key, None, [{"object": "GA1", "quantity": 5}])

        assert_that(result.for_sale_config.for_sale).is_false()
        assert_that(result.for_sale_config.area_places).is_equal_to({"GA1": 5})