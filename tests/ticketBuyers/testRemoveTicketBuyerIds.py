from uuid import uuid4

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RemoveTicketBuyerIdsTest(SeatsioClientTest):

    def test_can_remove_ticket_buyer_ids(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()
        ticket_buyer_id3 = uuid4()

        self.client.ticket_buyers.add([ticket_buyer_id1, ticket_buyer_id2])

        response = self.client.ticket_buyers.remove([ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3])

        assert_that(response.removed).contains_exactly_in_any_order(ticket_buyer_id1, ticket_buyer_id2)
        assert_that(response.not_present).contains_exactly_in_any_order(ticket_buyer_id3)

    def test_null_does_not_get_removed(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()
        ticket_buyer_id3 = uuid4()

        self.client.ticket_buyers.add([ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3])

        response = self.client.ticket_buyers.remove([ticket_buyer_id1, None])

        assert_that(response.removed).contains_exactly_in_any_order(ticket_buyer_id1)
        assert_that(response.not_present).is_empty()
