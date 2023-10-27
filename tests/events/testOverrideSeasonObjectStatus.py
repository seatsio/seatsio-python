from seatsio.domain import EventObjectInfo
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class OverrideSeasonObjectStatusTest(SeatsioClientTest):

    def test(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key, event_keys=["event1"])
        self.client.events.book(season.key, ["A-1", "A-2"])

        self.client.events.override_season_object_status("event1", ["A-1", "A-2"])

        a1_status = self.client.events.retrieve_object_info("event1", "A-1").status
        a2_status = self.client.events.retrieve_object_info("event1", "A-2").status

        assert_that(a1_status).is_equal_to(EventObjectInfo.FREE)
        assert_that(a2_status).is_equal_to(EventObjectInfo.FREE)
