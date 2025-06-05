from uuid import uuid4

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListTicketBuyerIdsTest(SeatsioClientTest):

    def test_can_list_ticket_buyer_ids(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()
        ticket_buyer_id3 = uuid4()

        self.client.ticket_buyers.add([ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3])

        ticket_buyer_ids = list(self.client.ticket_buyers.list_all())

        assert_that(ticket_buyer_ids).contains_exactly_in_any_order(ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3)

    def test_can_list_ticket_buyer_ids_more_than_one_page(self):
        ticket_buyer_ids_to_add = [uuid4() for _ in range(2400)]

        for i in range(0, len(ticket_buyer_ids_to_add), 1000):
            batch = ticket_buyer_ids_to_add[i:i + 1000]
            self.client.ticket_buyers.add(batch)

        ticket_buyer_ids = list(self.client.ticket_buyers.list_all())

        assert_that(ticket_buyer_ids).contains_exactly_in_any_order(*ticket_buyer_ids_to_add)
