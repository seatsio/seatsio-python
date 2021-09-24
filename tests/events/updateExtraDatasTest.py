from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateExtraDatasTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        extra_data1 = {"foo1": "bar1"}
        extra_data2 = {"foo2": "bar2"}

        self.client.events.update_extra_datas(event.key, {"A-1": extra_data1, "A-2": extra_data2})

        object_status1 = self.client.events.retrieve_object_info(event.key, "A-1")
        assert_that(object_status1.extra_data).is_equal_to(extra_data1)
        object_status2 = self.client.events.retrieve_object_info(event.key, "A-2")
        assert_that(object_status2.extra_data).is_equal_to(extra_data2)
