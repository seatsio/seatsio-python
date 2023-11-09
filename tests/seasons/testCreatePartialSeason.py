from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreatePartialSeasonTest(SeatsioClientTest):

    def test_partial_season_key_is_optional(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key)

        partial_season = self.client.seasons.create_partial_season(season.key, partial_season_key="aPartialSeason")

        assert_that(partial_season.key).is_equal_to("aPartialSeason")
        assert_that(partial_season.is_partial_season).is_true()
        assert_that(partial_season.top_level_season_key).is_equal_to(season.key)

    def test_event_keys_is_optional(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key, event_keys=["event1", "event2"])

        partial_season = self.client.seasons.create_partial_season(season.key, event_keys=["event1", "event2"])

        assert_that(partial_season.events)\
            .extracting("key")\
            .contains_exactly("event1", "event2")
        assert_that(partial_season.events[0].partial_season_keys_for_event).contains_exactly(partial_season.key)
