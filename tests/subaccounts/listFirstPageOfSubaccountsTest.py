from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListFirstPageOfSubaccountsTest(SeatsioClientTest):

    def test_allOnFirstPage(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list_first_page()

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount3.id, subaccount2.id, subaccount1.id)
        assert_that(subaccounts.next_page_starts_after).is_none()
        assert_that(subaccounts.previous_page_ends_before).is_none()

    def test_someOnFirstPage(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list_first_page(page_size=2)

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount3.id, subaccount2.id)
        assert_that(subaccounts.next_page_starts_after).is_equal_to(subaccount2.id)
        assert_that(subaccounts.previous_page_ends_before).is_none()
