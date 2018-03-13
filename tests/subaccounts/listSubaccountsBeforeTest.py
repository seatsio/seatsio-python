from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListSubaccountsBeforerTest(SeatsioClientTest):

    def test_withPreviousPage(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list().page_before(subaccount1.id)

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount3.id, subaccount2.id)
        assert_that(subaccounts.next_page_starts_after).is_equal_to(subaccount2.id)
        assert_that(subaccounts.previous_page_ends_before).is_none()

    def test_withNextAndPreviousPages(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list().set_page_size(1).page_before(subaccount1.id)

        assert_that(subaccounts.items).extracting("id").contains_exactly(subaccount2.id)
        assert_that(subaccounts.next_page_starts_after).is_equal_to(subaccount2.id)
        assert_that(subaccounts.previous_page_ends_before).is_equal_to(subaccount2.id)
