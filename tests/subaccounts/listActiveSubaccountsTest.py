from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListActiveSubaccountsTest(SeatsioClientTest):

    def test(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()
        self.client.subaccounts.deactivate(subaccount2.id)

        active_subaccounts = self.client.subaccounts.active.list()

        assert_that(active_subaccounts).extracting("id").contains_exactly(subaccount3.id, subaccount1.id, self.subaccount.id)
