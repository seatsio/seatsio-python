from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListStatusChangesForObjectTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        event = self.client.events.create(chart_key)

        self.client.events.change_object_status(event.key, ["A-1"], "status1")
        self.client.events.change_object_status(event.key, ["A-1"], "status2")
        self.client.events.change_object_status(event.key, ["A-1"], "status3")
        self.client.events.change_object_status(event.key, ["A-1"], "status4")

        status_changes = self.client.events.status_changes_for_object(event.key, "A-1").list()

        assert_that(status_changes).extracting("status").contains_exactly("status4", "status3", "status2", "status1")
