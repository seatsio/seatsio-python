from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class AddEventsToPartialSeasonTest(SeatsioClientTest):

    def test_add_events_to_partial_season(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key, event_keys=["event1", "event2"])
        partial_season = self.client.seasons.create_partial_season(season.key)

        updated_partial_season = self.client.seasons.add_events_to_partial_season(season.key, partial_season.key, ["event1", "event2"])

        assert_that(updated_partial_season.events).extracting("key").contains_exactly("event1", "event2")
        assert_that(updated_partial_season.events[0].partial_season_keys_for_event).contains_exactly(updated_partial_season.key)
