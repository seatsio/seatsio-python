from datetime import datetime, timedelta

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class CreateHoldTokenTest(SeatsioClientTest):

    def test(self):
        creation_time = datetime.utcnow()

        hold_token = self.client.hold_tokens.create()

        assert_that(hold_token.hold_token).is_not_none()

        assert_that(hold_token.expires_at) \
            .is_instance(datetime) \
            .is_between(creation_time + timedelta(minutes=15), creation_time + timedelta(minutes=16))

    def test_expires_in_minutes(self):
        creation_time = datetime.utcnow()

        hold_token = self.client.hold_tokens.create(5)

        assert_that(hold_token.hold_token).is_not_none()

        assert_that(hold_token.expires_at) \
            .is_instance(datetime) \
            .is_between(creation_time + timedelta(minutes=5), creation_time + timedelta(minutes=6))
