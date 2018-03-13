from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ListAllSubaccountsTest(SeatsioClientTest):

    def test_onePage(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list().all()

        assert_that(subaccounts).extracting("id").contains_exactly(subaccount3.id, subaccount2.id, subaccount1.id)

    def test_multiplePages(self):
        subaccount1 = self.client.subaccounts.create()
        subaccount2 = self.client.subaccounts.create()
        subaccount3 = self.client.subaccounts.create()

        subaccounts = self.client.subaccounts.list().set_page_size(1).all()

        assert_that(subaccounts).extracting("id").contains_exactly(subaccount3.id, subaccount2.id, subaccount1.id)