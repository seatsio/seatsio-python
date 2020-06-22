from seatsio import SocialDistancingRuleset
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class SaveSocialDistancingRulesetsTest(SeatsioClientTest):

    def test(self):
        chart = self.client.charts.create()
        rulesets = {
            'ruleset1': SocialDistancingRuleset(
                name='My first ruleset',
                number_of_disabled_seats_to_the_sides=1,
                disable_seats_in_front_and_behind=True,
                number_of_disabled_aisle_seats=2,
                max_group_size=1,
                disabled_seats=["A-1"],
                enabled_seats=["A-2"],
                index=4
            ),
            'ruleset2': SocialDistancingRuleset(name='My second ruleset'),
        }
        self.client.charts.save_social_distancing_rulesets(chart.key, rulesets)

        retrieved_chart = self.client.charts.retrieve(chart.key)
        assert_that(retrieved_chart.social_distancing_rulesets).is_equal_to(rulesets)
