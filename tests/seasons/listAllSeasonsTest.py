from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllSeasonsTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        season1 = self.client.seasons.create(chart.key)
        season2 = self.client.seasons.create(chart.key)
        season3 = self.client.seasons.create(chart.key)

        seasons = self.client.seasons.list()

        assert_that(seasons).extracting("key").contains_exactly(season3.key, season2.key, season1.key)
