from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class ActivateSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")
        self.client.subaccounts.deactivate(subaccount.id)

        self.client.subaccounts.activate(subaccount.id)

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.active).is_true()
