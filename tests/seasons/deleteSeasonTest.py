from datetime import datetime

from seatsio import SocialDistancingRuleset, TableBookingConfig
from seatsio.exceptions import SeatsioException
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class DeleteSeasonTest(SeatsioClientTest):

    def test_delete_season(self):
        chart_key = self.create_test_chart()
        season = self.client.seasons.create(chart_key)

        self.client.seasons.delete(season.key)

        try:
            self.client.seasons.retrieve(season.key)
            self.fail("expected an exception")
        except SeatsioException as e:
            assert_that(e.message).contains("404")
