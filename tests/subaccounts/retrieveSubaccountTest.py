from tests.seatsioClientTest import SeatsioClientTest
from tests.util.asserts import assert_that


class RetrieveSubaccountTest(SeatsioClientTest):

    def test(self):
        subaccount = self.client.subaccounts.create("joske")

        retrieved_subaccount = self.client.subaccounts.retrieve(subaccount.id)

        assert_that(retrieved_subaccount.id).is_equal_to(subaccount.id)
        assert_that(retrieved_subaccount.secret_key).is_not_blank()
        assert_that(retrieved_subaccount.designer_key).is_not_blank()
        assert_that(retrieved_subaccount.public_key).is_not_blank()
        assert_that(retrieved_subaccount.name).is_equal_to("joske")
        assert_that(retrieved_subaccount.active).is_true()
        assert_that(retrieved_subaccount.workspace).is_not_none()
        assert_that(retrieved_subaccount.workspace.id).is_not_none()
        assert_that(retrieved_subaccount.workspace.key).is_not_blank()
