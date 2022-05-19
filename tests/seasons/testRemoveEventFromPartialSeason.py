from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RemoveEventFromPartialSeasonTest(SeatsioClientTest):

    def test_remove_event_from_partial_season(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key, event_keys=["event1", "event2"])
        partial_season = self.client.seasons.create_partial_season(season.key, event_keys=["event1", "event2"])

        updated_partial_season = self.client.seasons.remove_event_from_partial_season(season.key, partial_season.key, "event2")

        assert_that(updated_partial_season.events).extracting("key").contains_exactly("event1")
