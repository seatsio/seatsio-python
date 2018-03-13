from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class UpdateSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")

        self.client.subaccounts.update(subaccount.id, "jefke")

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)
        assert_that(retrieved_subaccount.name).is_equal_to("jefke")
