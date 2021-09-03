from datetime import datetime, timedelta

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveHoldTokenTest(SeatsioClientTest):

    def test(self):
        hold_token = self.client.hold_tokens.create()

        retrieved_hold_token = self.client.hold_tokens.retrieve(hold_token.hold_token)

        assert_that(retrieved_hold_token.hold_token).is_equal_to(hold_token.hold_token)
        assert_that(retrieved_hold_token.expires_at).is_equal_to(hold_token.expires_at)
        assert_that(retrieved_hold_token.expires_in_seconds).is_between(14 * 60, 15 * 60)
        assert_that(retrieved_hold_token.workspace_key).is_not_none()
