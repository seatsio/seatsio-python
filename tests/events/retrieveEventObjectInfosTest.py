from seatsio.domain import EventObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveEventObjectInfosTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        object_infos = self.client.events.retrieve_object_infos(event.key, ["A-1", "A-2"])

        assert_that(object_infos["A-1"].status).is_equal_to(EventObjectInfo.FREE)
        assert_that(object_infos["A-2"].status).is_equal_to(EventObjectInfo.FREE)
        assert_that(object_infos).has_size(2)

    def test_holds(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()
        self.client.events.hold(event.key, 'GA1', hold_token.hold_token)

        object_infos = self.client.events.retrieve_object_infos(event.key, ["GA1"])

        expected_holds = {hold_token.hold_token: {"NO_TICKET_TYPE": 1}}
        assert_that(object_infos["GA1"].holds).is_equal_to(expected_holds)
