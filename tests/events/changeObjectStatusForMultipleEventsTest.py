from seatsio.domain import ObjectStatus, SocialDistancingRuleset
from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ChangeBestAvailableObjectStatusTest(SeatsioClientTest):

    def test_customStatus(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.change_object_status(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
            status="stat"
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to("stat")
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to("stat")
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to("stat")
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to("stat")

    def test_book(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.book(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(ObjectStatus.BOOKED)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(ObjectStatus.BOOKED)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(ObjectStatus.BOOKED)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(ObjectStatus.BOOKED)

    def test_hold(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)
        hold_token = self.client.hold_tokens.create()

        self.client.events.hold(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
            hold_token=hold_token.hold_token
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(ObjectStatus.HELD)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(ObjectStatus.HELD)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(ObjectStatus.HELD)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(ObjectStatus.HELD)

    def test_release(self):
        chart_key = self.create_test_chart()
        event1 = self.client.events.create(chart_key)
        event2 = self.client.events.create(chart_key)

        self.client.events.book(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        self.client.events.release(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1", "A-2"],
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(ObjectStatus.FREE)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(ObjectStatus.FREE)
        assert_that(self.fetch_status(event1.key, "A-2")).is_equal_to(ObjectStatus.FREE)
        assert_that(self.fetch_status(event2.key, "A-2")).is_equal_to(ObjectStatus.FREE)

    def fetch_status(self, event, o):
        return self.client.events.retrieve_object_status(event, o).status

    def test_ignoreSocialDistancing(self):
        chart_key = self.create_test_chart()
        rulesets = {
            'ruleset': SocialDistancingRuleset.fixed(
                name='My first ruleset',
                disabled_seats=["A-1"]
            )
        }
        self.client.charts.save_social_distancing_rulesets(chart_key, rulesets)
        event1 = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset')
        event2 = self.client.events.create(chart_key, social_distancing_ruleset_key='ruleset')

        self.client.events.book(
            event_key_or_keys=[event1.key, event2.key],
            object_or_objects=["A-1"],
            ignore_social_distancing=True
        )

        assert_that(self.fetch_status(event1.key, "A-1")).is_equal_to(ObjectStatus.BOOKED)
        assert_that(self.fetch_status(event2.key, "A-1")).is_equal_to(ObjectStatus.BOOKED)
