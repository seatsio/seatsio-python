from uuid import uuid4

from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class AddTicketBuyerIdsTest(SeatsioClientTest):

    def test_can_add_ticket_buyer_ids(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()
        ticket_buyer_id3 = uuid4()

        response = self.client.ticket_buyers.add([ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3])

        assert_that(response.added).contains_exactly_in_any_order(ticket_buyer_id1, ticket_buyer_id2, ticket_buyer_id3)
        assert_that(response.already_present).is_empty()

    def test_can_add_ticket_buyer_ids_list_with_duplicates(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()

        response = self.client.ticket_buyers.add([
            ticket_buyer_id1, ticket_buyer_id1, ticket_buyer_id1,
            ticket_buyer_id2, ticket_buyer_id2
        ])

        assert_that(response.added).contains_exactly_in_any_order(ticket_buyer_id1, ticket_buyer_id2)
        assert_that(response.already_present).is_empty()

    def test_same_id_doesnt_get_added_twice(self):
        ticket_buyer_id1 = uuid4()
        ticket_buyer_id2 = uuid4()

        response = self.client.ticket_buyers.add([ticket_buyer_id1, ticket_buyer_id2])
        assert_that(response.added).contains_exactly_in_any_order(ticket_buyer_id1, ticket_buyer_id2)
        assert_that(response.already_present).is_empty()

        second_response = self.client.ticket_buyers.add([ticket_buyer_id1])
        assert_that(second_response.added).is_empty()
        assert_that(second_response.already_present).contains_exactly_in_any_order(ticket_buyer_id1)

    def test_null_does_not_get_added(self):
        ticket_buyer_id1 = uuid4()

        response = self.client.ticket_buyers.add([ticket_buyer_id1, None])
        assert_that(response.added).contains_exactly_in_any_order(ticket_buyer_id1)
        assert_that(response.already_present).is_empty()
