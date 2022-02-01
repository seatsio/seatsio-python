from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateEventsInSeasonTest(SeatsioClientTest):

    def test_event_keys(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key)

        updated_partial_season = self.client.seasons.create_events(season.key, event_keys=["event1", "event2"])

        assert_that(updated_partial_season.events).extracting("key").contains_exactly("event1", "event2")

    def test_number_of_events(self):
        chart = self.client.charts.create()
        season = self.client.seasons.create(chart.key)

        updated_partial_season = self.client.seasons.create_events(season.key, number_of_events=2)

        assert_that(updated_partial_season.events).has_size(2)
