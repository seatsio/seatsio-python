from datetime import datetime, timedelta

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateHoldTokenTest(SeatsioClientTest):

    def test(self):
        creation_time = datetime.utcnow()

        hold_token = self.client.hold_tokens.create()

        assert_that(hold_token.hold_token).is_not_none()

        now_plus_14 = creation_time + timedelta(minutes=14)
        now_plus_16 = creation_time + timedelta(minutes=16)
        assert_that(hold_token.expires_at)\
            .is_instance(datetime)\
            .is_between(now_plus_14, now_plus_16)
