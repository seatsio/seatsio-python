from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateExtraDataTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data = {"foo": "bar"}

        self.client.events.update_extra_data(event.key, "A-1", extra_data)

        object_status = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_status.extra_data).is_equal_to(extra_data)
