from datetime import datetime, timedelta

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateHoldTokenExpirationDateTest(SeatsioClientTest):

    def test(self):
        hold_token = self.client.hold_tokens.create()
        now = datetime.utcnow()

        updated_hold_token = self.client.hold_tokens.expire_in_minutes(hold_token.hold_token, 30)

        assert_that(updated_hold_token.hold_token).is_equal_to(hold_token.hold_token)

        now_plus_14 = now + timedelta(minutes=29)
        now_plus_16 = now + timedelta(minutes=31)
        assert_that(updated_hold_token.expires_at) \
            .is_instance(datetime) \
            .is_between(now_plus_14, now_plus_16)

        assert_that(updated_hold_token.expires_in_seconds).is_between(29 * 60, 30 * 60)
