from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllSubaccountsTest(SeatsioClientTest):

    def test(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list()

        assert_that(subaccounts).extracting("id").contains_exactly(subaccount3.id, subaccount2.id, subaccount1.id, self.subaccount.id)
