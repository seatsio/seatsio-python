from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)

        assert_that(retrieved_subaccount.id).is_equal_to(subaccount.id)
        assert_that(retrieved_subaccount.secretKey).is_not_blank()
        assert_that(retrieved_subaccount.designerKey).is_not_blank()
        assert_that(retrieved_subaccount.publicKey).is_not_blank()
        assert_that(retrieved_subaccount.name).is_equal_to("joske")
        assert_that(retrieved_subaccount.active).is_true()
